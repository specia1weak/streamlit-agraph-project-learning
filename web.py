import streamlit as st
from streamlit_agraph import Edge, Node, agraph, Config
from streamlit_utils.global_var import VarInStreamlit
from AllocateGraph import AllocateGraph
import os
import re

st.set_page_config(layout="wide")

graph_txt = "test.txt"
mid_txt = "mid.txt"


def global_var(name, init_obj=None, init_fn=None):
    var = VarInStreamlit(st, name, init_obj, init_fn)
    return var


print("————————————————————刷新——————————————————")

allocate_graph_var = global_var("_allocate_graph", AllocateGraph(graph_txt))
cfg_var = global_var("_config", Config(height=600, width=800,
                                       physics=True, hierarchical=False,
                                       repulsion={
                                           "centralGravity": 0.01,
                                           "nodeDistance": 100
                                       }
                                       ))
graph_nodes_var = global_var("_graph_nodes", None)
graph_edges_var = global_var("_graph_edges", None)
need_reload_var = global_var("_need_reload", True)

pre_selected_node_var = global_var("_pre_selected_node", None)

# @@@@@@@@@按钮信号@@@@@@@@@
delete_clicked_var = global_var("_delete_clicked", False)
delete_step_var = global_var("_delete_step", 0)

add_edge_clicked_var = global_var("_add_edge_clicked", False)
add_edge_step_var = global_var("_add_edge_step", 0)
edge_src_var = global_var("edge_src", None)
edge_tar_var = global_var("edge_tar", None)

# delete_clicked_var = global_var("_delete_clicked", False)
# delete_clicked_var = global_var("_delete_clicked", False)
# delete_clicked_var = global_var("_delete_clicked", False)
show_non_block_var = global_var("_show_non_block", False)
delete_non_block_var = global_var("_delete_non_block", False)
non_block_nodes_var = global_var("_non_block_nodes_var", [])
if need_reload_var.val:
    print("@@@@@@@重载@@@@@@@@@@")
    need_reload_var.val = False
    proc_color = "#00CED1"  # （蔚蓝色）
    req_color = "#9370DB"  # （紫罗兰色）
    alloc_color = "#FFD700"  # （金色）
    reso_color = "#FFA07A"  # （浅鲑鱼色）
    non_block_color = "#FF6347"  # （番茄红）
    nodes, edges = allocate_graph_var.val.get_graph_data(
        proc_color, req_color, alloc_color, reso_color, non_block_nodes_var.val, non_block_color
    )
    graph_nodes_var.val = nodes
    graph_edges_var.val = edges

col1, col2 = st.columns([6, 4])

with col1:
    st.subheader("资源分配图")
with col2:
    st.subheader("操作面板")
col1, col2 = st.columns([6, 4])
with col1:
    selected_node = agraph(graph_nodes_var.val, graph_edges_var.val, cfg_var.val)
    print(selected_node)
    # 下面这玩意要承担很多东西
    col3, col4 = st.columns([1, 15])
    with col3:
        st.text("信息：")
    with col4:
        space_hold = st.empty()

id_var = global_var("_id")
value_var = global_var("_value")
proc_or_reso_var = global_var("_proc_or_reso")
add_node_signal_var = global_var("_add_node_signal")
with col2:
    st.markdown("资源图化简")
    col1, col2, col3 = st.columns([2, 2.5, 2])
    with col1:
        if st.button("显示非阻塞结点"):
            print("点击显示非阻塞结点, 以前是否点击过", show_non_block_var.val)
            if not show_non_block_var.val:
                show_non_block_var.val = True
                allocate_graph_var.val.save_as_txt(graph_txt)
                print("执行计算更新！")
                os.system("exec.exe {} {}".format(graph_txt, mid_txt))
            with open(mid_txt, 'r', encoding="utf8") as f:
                nums = list(map(int, re.split(r"\W+", f.read().strip())))
            print("calc信息", nums)
            non_block_flag = nums[0] > 0
            num_non_block_node = nums[1]
            print("是否结束", num_non_block_node == 0)
            non_block_nodes_var.val = nums[2:]
            if num_non_block_node == 0:
                st.info("资源图已最简")
                if not non_block_flag:
                    st.warning("检测到死锁")
                    procs, resos = allocate_graph_var.val.ret()
                    st.write("死锁进程", procs)
                    st.write("死锁资源", resos)
            need_reload_var.val = True

            # 把结点读出mid.txt 传参，重新搞图
    with col2:
        if st.button("删除非阻塞节点相关边"):
            print("删除非阻塞节点相关边")
            if not show_non_block_var.val:
                allocate_graph_var.val.save_as_txt(graph_txt)
                os.system("exec.exe {} {}".format(graph_txt, mid_txt))
            allocate_graph_var.val.init_graph(graph_txt)
            show_non_block_var.val = False
            need_reload_var.val = True
            non_block_nodes_var.val = []
    with col3:
        st.button("刷新图谱", type="primary")


    st.divider()
    st.markdown("资源图更改")
    with st.form("增加节点"):
        node_type = ("进程", "资源")


        def add_node():
            print("增加")
            add_node_signal_var.val = True


        selected_type = st.selectbox("增加结点", node_type)
        cola, colb = st.columns(2)
        with cola:
            id_var.val = st.number_input("id号", min_value=1, max_value=255, )
        with colb:
            value_var.val = st.number_input("资源数量(如果增加资源)", min_value=1, max_value=255, )

        proc_or_reso_var.val = selected_type
        st.form_submit_button("确定增加", on_click=add_node)
    st.divider()
    col1, col2, col3, col4, col5 = st.columns([1, 0.5, 0.5, 1.2, 1])
    with col1:
        def delete_node():
            if selected_node is None:
                return
            if 'r' == str(selected_node[0]).lower():
                allocate_graph_var.val.del_reso(selected_node[1:])
            elif 'p' == str(selected_node[0]).lower():
                allocate_graph_var.val.del_proc(selected_node[1:])
            need_reload_var.val = True


        st.button("删除结点", on_click=delete_node)

        if st.button("增加边"):
            add_edge_clicked_var.val = True
            add_edge_step_var.val = 1
            edge_src_var.val = None
            edge_tar_var.val = None
    with col2:
        st.text("起始：")
        if add_edge_clicked_var.val and add_edge_step_var.val == 1:
            edge_src_var.val = selected_node
            add_edge_step_var.val = 2

        if edge_src_var.val:
            st.text(edge_src_var.val)
        else:
            st.text("")
    with col3:
        st.text("结束：")
        if add_edge_clicked_var.val and add_edge_step_var.val == 2 and pre_selected_node_var.val != selected_node:
            edge_tar_var.val = selected_node
            add_edge_clicked_var.val = False
            add_edge_step_var.val = 0
        if edge_tar_var.val:
            st.text(edge_tar_var.val)
        else:
            st.text("")
    with col4:
        value = st.number_input("请求（占用）值：", min_value=1, max_value=200)
    with col5:
        def add_edge():
            a = edge_src_var.val
            b = edge_tar_var.val
            if not a or not b:
                return
            edge_src_var.val = None
            edge_tar_var.val = None
            print(a, b)
            ret = False
            if a[0].lower() == 'r' and b[0].lower() == 'p':
                ret = allocate_graph_var.val.add_alloc(b[1:], a[1:], value)
            elif a[0].lower() == 'p' and b[0].lower() == 'r':
                ret = allocate_graph_var.val.add_req(a[1:], b[1:], value)
            else:
                st.warning("关系必须是进程与资源之间的")
            if ret:
                need_reload_var.val = True
                print("完成")


        st.button("确认更改", key="_确认更改", on_click=add_edge)

    st.divider()
    if st.button("保存到文件中(请在修改图谱后点击保存)", type="primary"):
        allocate_graph_var.val.save_as_txt(graph_txt)
        need_reload_var.val = True
        print("保存成功")
        show_non_block_var.val = False

with space_hold:
    if add_edge_clicked_var.val:
        if add_edge_step_var.val == 2:
            st.write("请选择结束结点")
    else:
        st.write("选中", selected_node)

if add_node_signal_var.val:
    add_node_signal_var.val = False
    if proc_or_reso_var.val == "进程":
        print(allocate_graph_var.val.add_proc(id_var.val))
        need_reload_var.val = True
    elif proc_or_reso_var.val == "资源":
        print(allocate_graph_var.val.add_reso(id_var.val, value_var.val))
        need_reload_var.val = True
    st.rerun()

pre_selected_node_var.val = selected_node

st.markdown("""
<style>
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi2 > div > div > div > div:nth-child(2) > div.st-emotion-cache-fplge5.e1f1d6gn3
{
    border: 2px solid #964B00;
}
</style>
""", unsafe_allow_html=True)
