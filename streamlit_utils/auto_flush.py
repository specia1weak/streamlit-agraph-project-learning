import streamlit as st
import streamlit_autorefresh
from streamlit_utils.global_var import VarInStreamlit

def global_var(name, init_obj=None, init_fn=None):
    var = VarInStreamlit(st, name, init_obj=init_obj, init_fn=init_fn)
    return var


flush_interval = global_var("flush_interval", None)
def update_flush_speed(interval=0, limit=None, debounce=False, key=None):
    """
    :param interval: 时间间隔，特殊值None表示停止，0表示继续刷新，间隔不变
    :param limit: 次数
    :param debounce: 不知道
    :param key: 不知道
    :return: None
    """
    if interval is not None and interval > 0:
        flush_interval.val = interval
    if interval is None:
        flush_interval.val = None
    if flush_interval.val is not None:
        streamlit_autorefresh.st_autorefresh(interval=flush_interval.val,
                                             limit=limit, debounce=debounce, key=key)
update_flush_speed()