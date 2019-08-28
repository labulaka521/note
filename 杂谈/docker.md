# Docker的一些底层的原理

Linux上的命名空间(NameSpaces)、控制组(Control Group)、Union文件系统(Union file system)和容器格式(Container Format)

## NameSpaces命名空间
命名空间是linux为我们提供用于分离进程树、网络接口、挂载点以及进程间通信资源的方法，Docker通过Linux的namespaces对不同的容器进行了隔离，但是命名空间不能提供物理资源的隔离  
Linux提供了以下的命名空间
- CLONE_NEWCGROUP
- CLONE_NEWIPC
- CLONE_NEWNET
- CLONE_NEWS
- CLONE_NEWPID
- CLONE_NEWUSER
- CLONE_NEWUTS

命名空间是Linux内核强大的特性。每个容器都有自已单独的命名空间，运行在其中的应用都像是在独立的操作系统中运行一样。命名空间保证了容器之间彼此互不影响
- pid命名空间
- net命名空间
- ipc命名空间
- mnt命名空间
- uts命名空间
- user命名空间

## CGroups控制组
控制组是Linux内核的一个特性,主要用来对共享资源进行隔离、限制、审计等。只有能控制分配到容器的资源，才能避免当多个容器同时运行时对系统资源的竞争。
Cgroups是用来进行隔离限制物理资源的，这样就可以为每个Docker容器来设置物理资源的使用大小，以防止在一些场景下，将宿主的物理资源如网络、CPU等资源占用过多    
控制组可以提供对容器的内存、CPU、磁盘IO等资源的限制和审计管理

## UnionFS联合文件系统
将多个文件系统联合到同一个挂载点的文件服务，镜像是只读的，容器是可以修改的，每一层镜像层都是建立在另一层的镜像层之上  
联合文件系统是一种分层、轻量级并且高性能的文件系统，它支持对文件系统的修改作为一次一次提交来一层层的叠加，同时可以将不同的目录挂载到同一虚拟文件系统下  


docker与虚拟机的区别  
虚拟机是在硬件级别进行虚拟化，模拟硬件搭建操作系统，而Docker是在操作系统的层面虚拟化，复用操作系统，  
虚拟机实现了操作系统方面的隔离，Docker实现了进程之间的隔离  
虚拟级是在Hypervisor上运行的Gustos 上运行的各种服务，Docker则是在Docker Daemon上的各种容器