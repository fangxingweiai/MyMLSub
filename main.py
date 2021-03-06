import sys
from typing import Union, List

from loguru import logger

import settings
from core.config_model import ProxyNode
from core.converter import load_resources, change_host, generate_sub, save_conf, sub_2_nodelist
from core.helper import get_request

# 设置日志
logger_level = settings.log_level
logger.remove()
logger.add(sys.stdout, level=logger_level)

request = get_request(settings.enable_proxy, settings.proxies)


def resolve_proxies(proxies: Union[str, List]) -> List:
    if isinstance(proxies, str):
        proxies = [proxies]

    nodes = []
    for i in proxies:
        if isinstance(i, str):
            i = i.strip()
            if i.startswith("http"):
                logger.info(f"开始获取订阅{i}的内容")
                try:
                    sub_content = request(i)
                    logger.debug(f"获取订阅的内容为: {sub_content}")
                except Exception as e:
                    logger.error(f"获取订阅内容出错: {e}")
                    continue

                if sub_content:
                    node_list = sub_2_nodelist(sub_content)
                    nodes.extend(node_list)
            else:
                vn = ProxyNode()
                logger.debug('检查v2节点有效性')
                if vn.load(i):
                    logger.info(f"v2节点，直接添加: {i}")
                    nodes.append(vn)
    return nodes


def main():
    host = settings.ml_host  # 'short.pay.weixin.qq.com'
    clients = ['Clash', 'Surfboard', 'v2rayN', 'Leaf']
    resources = load_resources()
    logger.info(f"用户需要转换的内容：{resources}")

    nodes = resolve_proxies(resources)

    logger.info(f"用户输入有效节点总个数为: {len(nodes)}")

    if nodes:
        logger.info(f"将过滤完的节点的host用{host}替换")
        change_host(nodes, host)

        for client in clients:
            logger.info(f'开始生成{client}订阅')
            sub = generate_sub(nodes, client)

            if sub:
                logger.info(f'保存订阅至文件{settings.conf_dir}/{client}')
                save_conf(sub, settings.conf_dir, client)


if __name__ == '__main__':
    main()
