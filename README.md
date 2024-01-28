# addns

动态更新阿里云域名实现ddns功能

```
docker run -d --name ddns \
 -e ACCESS_KEY_ID=your_aliyun_access_key_id\
 -e ACCESS_KEY=your_aliyun_access_key\
 -e DOMAIN=your_dynamic_domain\
 ddns
```

