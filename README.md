# ssh-runner record.

```
docker run --env=DRONE_RPC_PROTO=http \
--env=DRONE_RPC_HOST=? \
--env=DRONE_RPC_SECRET=? \
--env=DRONE_UI_DISABLED=false \
--env=DRONE_UI_USERNAME=root \
--env=DRONE_UI_PASSWORD=root \
--env=DRONE_HTTP_HOST=?:3000 \
--env=DRONE_HTTP_PROTO=http \
--publish=3000:3000 \
--restart always \
--name drone-runner drone/drone-runner-ssh
```