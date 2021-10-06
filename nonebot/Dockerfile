FROM python:3.8.10-alpine

COPY ./ ./

RUN python3 -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip3 install "nonebot[scheduler]" requests redis Quart-CORS -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk update \
    && apk add openjdk8 curl busybox tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo Asia/Shanghai > /etc/timezone \
    && apk del tzdata \
    && rm -rf /tmp/* /var/cache/apk/*