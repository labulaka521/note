golang sql连接池由于设置空间连接比较少最大连接数太多导致的Time Wait

golang sql初始化可以设置最大连接数，也可以设置最大连接空闲数

先看获取一个连接的`Conn`函数
```go
func (db *DB) Conn(ctx context.Context) (*Conn, error) {
	var dc *driverConn
    var err error
    // 尝试获取两次
    // 
	for i := 0; i < maxBadConnRetries; i++ {
		dc, err = db.conn(ctx, cachedOrNewConn)
		if err != driver.ErrBadConn {
			break
		}
    }
    
	if err == driver.ErrBadConn {
		dc, err = db.conn(ctx, cachedOrNewConn)
	}
	if err != nil {
		return nil, err
	}

	conn := &Conn{
		db: db,
		dc: dc,
	}
	return conn, nil
}
```

获取连接主要在`db.conn`这个函数  
```go
// conn returns a newly-opened or cached *driverConn.
func (db *DB) conn(ctx context.Context, strategy connReuseStrategy) (*driverConn, error) {
	db.mu.Lock()
	if db.closed {
		db.mu.Unlock()
		return nil, errDBClosed
	}
	// 检查context是否取消
	select {
	default:
	case <-ctx.Done():
		db.mu.Unlock()
		return nil, ctx.Err()
	}
	lifetime := db.maxLifetime

	// 先从闲置连接中获取一个连接
	numFree := len(db.freeConn)
	if strategy == cachedOrNewConn && numFree > 0 {
		conn := db.freeConn[0]
		copy(db.freeConn, db.freeConn[1:])
		db.freeConn = db.freeConn[:numFree-1]
		conn.inUse = true
        db.mu.Unlock()
        // 判断连接是否失效
		if conn.expired(lifetime) {
			conn.Close()
			return nil, driver.ErrBadConn
		}
		// Lock around reading lastErr to ensure the session resetter finished.
		conn.Lock()
		err := conn.lastErr
		conn.Unlock()
		if err == driver.ErrBadConn {
			conn.Close()
			return nil, driver.ErrBadConn
		}
		return conn, nil
	}

	// Out of free connections or we were asked not to use one. If we're not
    // allowed to open any more connections, make a request and wait.
    // 如果设置了最大的连接数，而且现在的连接数比大于等于最大的连接数时，则会阻塞等待连接释放，或者context取消
	if db.maxOpen > 0 && db.numOpen >= db.maxOpen {
		// Make the connRequest channel. It's buffered so that the
		// connectionOpener doesn't block while waiting for the req to be read.
		req := make(chan connRequest, 1)
		reqKey := db.nextRequestKeyLocked()
		db.connRequests[reqKey] = req
		db.waitCount++
		db.mu.Unlock()

		waitStart := time.Now()

		// Timeout the connection request with the context.
		select {
		case <-ctx.Done():
			// Remove the connection request and ensure no value has been sent
			// on it after removing.
			db.mu.Lock()
			delete(db.connRequests, reqKey)
			db.mu.Unlock()

			atomic.AddInt64(&db.waitDuration, int64(time.Since(waitStart)))

			select {
			default:
			case ret, ok := <-req:
				if ok && ret.conn != nil {
					db.putConn(ret.conn, ret.err, false)
				}
			}
			return nil, ctx.Err()
		case ret, ok := <-req:
			atomic.AddInt64(&db.waitDuration, int64(time.Since(waitStart)))

			if !ok {
				return nil, errDBClosed
			}
			if ret.err == nil && ret.conn.expired(lifetime) {
				ret.conn.Close()
				return nil, driver.ErrBadConn
			}
			if ret.conn == nil {
				return nil, ret.err
			}
			// Lock around reading lastErr to ensure the session resetter finished.
			ret.conn.Lock()
			err := ret.conn.lastErr
			ret.conn.Unlock()
			if err == driver.ErrBadConn {
				ret.conn.Close()
				return nil, driver.ErrBadConn
			}
			return ret.conn, ret.err
		}
	}
    // 如果还是不行就新创建一个连接
	db.numOpen++ // optimistically
	db.mu.Unlock()
	ci, err := db.connector.Connect(ctx)
	if err != nil {
		db.mu.Lock()
		db.numOpen-- // correct for earlier optimism
		db.maybeOpenNewConnections()
		db.mu.Unlock()
		return nil, err
	}
	db.mu.Lock()
	dc := &driverConn{
		db:        db,
		createdAt: nowFunc(),
		ci:        ci,
		inUse:     true,
	}
	db.addDepLocked(dc, dc)
	db.mu.Unlock()
	return dc, nil
}

```

在每次查询数据的时候先从从连接池或者新建一个连接，数据查询完毕后需要主动执行Close方法来关闭这个连接，此时的关闭连接不是单纯的关闭，而是先尝试将连接放到闲置连接池中，如果失败的话就关闭这个连接

操作是安全的，这个就是关闭连接的函数
```go
func (c *Conn) Close() error {
	return c.close(nil)
}
```
close方法检查连接是否已经关闭，然后释放这个连接
```go
func (c *Conn) close(err error) error {
    // 先使用cas获取连接是否已经关闭
	if !atomic.CompareAndSwapInt32(&c.done, 0, 1) {
		return ErrConnDone
	}

	// Lock around releasing the driver connection
    // to ensure all queries have been stopped before doing so.
    // 加锁 确保查询已经完成
	c.closemu.Lock()
	defer c.closemu.Unlock()
    // 这个函数主要是先尝试将连接放回闲置的连接池 如果失败就关闭连接
	c.dc.releaseConn(err)
	c.dc = nil
	c.db = nil
	return err
}
```
releaseConn就是释放连接的函数接受一个err类型的值,这个函数是调用putConn这个函数
```go
func (dc *driverConn) releaseConn(err error) {
	dc.db.putConn(dc, err, true)
}

func (db *DB) putConn(dc *driverConn, err error, resetSession bool) {
	db.mu.Lock()
	if !dc.inUse {
		if debugGetPut {
			fmt.Printf("putConn(%v) DUPLICATE was: %s\n\nPREVIOUS was: %s", dc, stack(), db.lastPut[dc])
		}
		panic("sql: connection returned that was never out")
	}
	if debugGetPut {
		db.lastPut[dc] = stack()
	}
	dc.inUse = false

	for _, fn := range dc.onPut {
		fn()
	}
	dc.onPut = nil

	if err == driver.ErrBadConn {
		// Don't reuse bad connections.
		// Since the conn is considered bad and is being discarded, treat it
		// as closed. Don't decrement the open count here, finalClose will
		// take care of that.
		db.maybeOpenNewConnections()
		db.mu.Unlock()
		dc.Close()
		return
	}
	if putConnHook != nil {
		putConnHook(db, dc)
	}
	if db.closed {
		// Connections do not need to be reset if they will be closed.
		// Prevents writing to resetterCh after the DB has closed.
		resetSession = false
	}
	if resetSession {
		if _, resetSession = dc.ci.(driver.SessionResetter); resetSession {
			// Lock the driverConn here so it isn't released until
			// the connection is reset.
			// The lock must be taken before the connection is put into
			// the pool to prevent it from being taken out before it is reset.
			dc.Lock()
		}
    }
    
    // 将连接归还给连接池 
	added := db.putConnDBLocked(dc, nil)
	db.mu.Unlock()
    // 归还失败的话就关闭这个连接
	if !added {
		if resetSession {
			dc.Unlock()
		}
		dc.Close()
		return
	}
	if !resetSession {
		return
	}
	select {
	default:
		// If the resetterCh is blocking then mark the connection
        // as bad and continue on.
        // 连接池满就标记这个连接为错误
		dc.lastErr = driver.ErrBadConn
        dc.Unlock()
    // 将连接放回channel
	case db.resetterCh <- dc:
	}
}

// Satisfy a connRequest or put the driverConn in the idle pool and return true
// or return false.
// putConnDBLocked will satisfy a connRequest if there is one, or it will
// return the *driverConn to the freeConn list if err == nil and the idle
// connection limit will not be exceeded.
// If err != nil, the value of dc is ignored.
// If err == nil, then dc must not equal nil.
// If a connRequest was fulfilled or the *driverConn was placed in the
// freeConn list, then true is returned, otherwise false is returned.
func (db *DB) putConnDBLocked(dc *driverConn, err error) bool {
	if db.closed {
		return false
	}
	if db.maxOpen > 0 && db.numOpen > db.maxOpen {
		return false
	}
	if c := len(db.connRequests); c > 0 {
		var req chan connRequest
		var reqKey uint64
		for reqKey, req = range db.connRequests {
			break
		}
		delete(db.connRequests, reqKey) // Remove from pending requests.
		if err == nil {
			dc.inUse = true
		}
		req <- connRequest{
			conn: dc,
			err:  err,
		}
		return true
	} else if err == nil && !db.closed {
		if db.maxIdleConnsLocked() > len(db.freeConn) {
			db.freeConn = append(db.freeConn, dc)
			db.startCleanerLocked()
			return true
		}
		db.maxIdleClosed++
	}
	return false
}
```

当空闲连接少的时候，最大连接又比较大，这时如果有大量的连接，就会造成大量的连接被关闭，导致产生大量的`Time-Wait`状态。
