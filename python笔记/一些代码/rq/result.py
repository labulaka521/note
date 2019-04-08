# 结果值过期时间
# result_ttl=10 作业完成后 会根据将job的hash值存入redis 默认500s后过期
# 可以设置result_ttl来指定默认时间后过期 设置为-1则永不过期
job = q.enqueue(count_words_at_url, 'https://github.com', result_ttl=10)

