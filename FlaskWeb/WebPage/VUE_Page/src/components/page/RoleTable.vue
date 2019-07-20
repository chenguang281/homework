<template>
    <div class="table">
        <div class="container">
            <div class="handle-box">
                <el-input v-model="select_word" placeholder="筛选关键词" class="handle-input mr10" clearable @keyup.enter.native="search"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="search">搜索</el-button>
                <el-button type="primary" icon="el-icon-plus" @click="add_page">新增</el-button>
            </div>
            <el-table :data="tableData" border class="table" ref="multipleTable" v-loading="loading">
<!--                <el-table-column prop="id" label="用户ID" width="150" v-if="hideRow">-->
<!--                </el-table-column>-->
                <el-table-column prop="role_name" label="角色名" width="150" align="center" sortable>
                </el-table-column>
                <el-table-column prop="describe" label="角色描述" width="240" align="center" sortable>
                </el-table-column>
                <el-table-column prop="create_time" label="创建时间" align="center" sortable>
                </el-table-column>
                <el-table-column prop="update_time" label="最后更新时间" align="center" sortable>
                </el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑
                        </el-button>
                        <el-button type="text" icon="el-icon-delete" class="red"
                                   @click="handleDelete(scope.$index, scope.row)">删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="nowPage"
                    :page-sizes=pageSizeArr
                    :page-size=pageSize
                    layout="total, sizes, prev, pager, next, jumper"
                    :total=total
                    class="pagination">
            </el-pagination>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="80%" v-loading="updateLoading">
            <el-container>
                <el-aside>
                    <el-form ref="form" :model="formUpdate" label-width="120px">
                        <el-form-item label="角色名称">
                            <el-input v-model="formUpdate.update_role_name"></el-input>
                        </el-form-item>
                        <el-form-item label="角色描述">
                            <el-input v-model="formUpdate.update_describe"></el-input>
                        </el-form-item>
                    </el-form>
                </el-aside>
                <el-main><!-- default-expand-all 展开所有节点-->
                    <el-tree
                            :props="dataModel"
                            :data="loadUpdateMenuNode"
                            node-key="id"
                            ref="update_tree"
                            :default-expanded-keys='checkMenu'
                            :default-checked-keys='checkMenu'
                            show-checkbox>
                    </el-tree>
                    <br>
                    <br>
                </el-main>
            </el-container>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 删除提示框 -->
        <el-dialog title="提示" :visible.sync="delVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteRow">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 新增弹出框 -->
        <el-dialog title="新增角色" :visible.sync="addVisible" width="80%" v-loading="addLoading">
            <el-container>
                <el-aside>
                    <el-form ref="form" :model="formAdd" label-width="120px">
                        <el-form-item label="角色名称">
                            <el-input v-model="formAdd.add_role_name"></el-input>
                        </el-form-item>
                        <el-form-item label="角色描述">
                            <el-input v-model="formAdd.add_describe"></el-input>
                        </el-form-item>
                    </el-form>
                </el-aside>
                <el-main><!-- default-expand-all 展开所有节点-->
                    <el-tree
                            v-loading="add_tree_loading"
                            :props="dataModel"
                            :load="loadMenuNode"
                            lazy
                            node-key="id"
                            ref="add_tree"
                            show-checkbox
                            :expand-on-click-node="false"
                    >
                    </el-tree>
                    <br>
                    <br>
                </el-main>
            </el-container>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addVisible = false">取 消</el-button>
                <el-button type="primary" @click="acceptAdd" v-loading="addLoadingBtn">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: 'basetable',
        data() {
            return {
                nowPage: 1,//初始化页数--当前页
                total: 0, //总条数
                pageSize: 10, //初始每页条数
                pageSizeArr: [10, 20, 50, 100],//每页展示条数数组


                checkMenu: [],
                loadUpdateMenuNode: [],//修改时候用的树
                hideRow: '',
                dataModel: {
                    label: 'menu_name',
                    children: 'children',
                    isLeaf: 'leaf'
                },
                add_tree_loading: false,
                is_search: false,
                tableData: [],
                select_word: '',
                editVisible: false,
                addVisible: false,
                delVisible: false,
                loading: true,
                addLoading: false,
                updateLoading: false,
                delId: '',
                //修改传递数据
                formUpdate: {
                    update_id: '',
                    update_role_name: '',
                    update_describe: '',
                    update_menu_id: '',
                },
                //新增传递数据
                formAdd: {
                    add_role_name: '',
                    add_describe: ''
                },
                addLoadingBtn:false,
            }
        },
        created() {
            let json = {
                nowPage: this.nowPage,
                pagesize: this.pageSize
            }
            this.$axios.post("/api/sys_role/get_role_list", json).then((res) => {
                this.tableData = res.data.data;
                this.total = res.data.total;
                this.loading = false;
            }).catch(function (error) {
                this.loading = false
                console.log("err==" + error);
            });
        },


        methods: {
            loadMenuNode(node, resolve) {
                this.add_tree_loading = true
                if (node.level === 0) {
                    let menu_data = []
                    let menu_json = {}
                    setTimeout(() => {
                        this.$axios.post("/api/sys_menu/get_menu_list_role", menu_json).then((res) => {
                            menu_data = res.data.data;
                            return resolve(menu_data);
                        }).catch(function (error) {
                            this.loading = false;
                            console.log("err==" + error);
                        });
                    }, 100);
                } else {
                    setTimeout(() => {
                        let menu_json = {menu_id: node.data.id}
                        this.$axios.post("/api/sys_menu/get_next_menu_list_role", menu_json).then((res) => {
                            const data = res.data.data
                            resolve(data);
                        }).catch(function (error) {
                            this.loading = false
                            console.log("err==" + error);
                        });
                    }, 1);
                }
                this.add_tree_loading = false;
                this.addLoading = false
            },

            search() {
                this.loading = true
                let json = {
                    role_name: this.select_word,
                    nowPage: this.nowPage,
                    pagesize: this.pageSize
                }
                this.$axios.post("/api/sys_role/get_role_list", json).then((res) => {
                    this.tableData = res.data.data
                    this.total = res.data.total
                    this.nowPage = res.data.nowPage
                    this.loading = false
                }).catch(function (error) {
                    this.loading = false
                    console.log("err==" + error);
                });
            },
            //新增弹出层
            add_page() {
                this.addLoadingBtn = false
                this.addLoading = true
                this.formAdd = {
                    add_role_name: '',
                    add_describe: '',
                }
                this.addVisible = true;
                this.addLoading = false
            },
            // 编辑展开页面
            handleEdit(index, row) {
                this.checkMenu = [];
                this.formUpdate = {
                    update_id: row.id,
                    update_role_name: row.role_name,
                    update_describe: row.describe,
                }
                //开始获得所有菜单
                let json = {update_id: row.id}
                // 取得已有权限
                this.$axios.post("/api/sys_role/get_role_permission", json).then((res) => {
                    this.checkMenu = res.data.data;
                }).catch(function (error) {
                    this.loading = false
                    console.log("err==" + error);
                });
                //取到所有菜单
                this.$axios.post("/api/sys_menu/get_all_menu", json).then((res) => {
                    this.loadUpdateMenuNode = this.toTree(res.data.data);
                    this.editVisible = true;
                }).catch(function (error) {
                    this.loading = false
                    console.log("err==" + error);
                });


            },

            // 保存编辑
            saveEdit() {
                this.updateLoading = true
                let json = {}
                json.update_id = this.formUpdate.update_id
                json.role_name = this.formUpdate.update_role_name
                json.describe = this.formUpdate.update_describe
                let menu_id = this.$refs.update_tree.getCheckedKeys();//选中的
                let menu_id_half = this.$refs.update_tree.getHalfCheckedKeys();//半选中的
                json.menu_id = menu_id
                json.menu_id_half = menu_id_half
                this.$axios.post("/api/sys_role/update_role", json).then((res) => {
                    this.updateLoading = false
                    if (res.data.code === '200' || res.data.code === 200) {
                        this.search()
                        this.$message.success('修改成功');
                        this.editVisible = false;
                    } else {
                        this.$message.error('修改失败');
                        this.editVisible = false;
                    }
                }).catch(function (error) {
                    this.updateLoading = false
                    this.$message.success('修改失败');
                    alert("err==" + error);
                    this.editVisible = false;
                });
            },

            //删除弹出
            handleDelete(index, row) {
                this.delId = row.id;
                this.idx = index;
                this.delVisible = true;
            },
            // 确定删除
            deleteRow() {
                let json = {role_id: this.delId};
                this.$axios.post("/api/sys_role/delete_role", json).then((res) => {
                    if (res.data.code === '200' || res.data.code === 200) {
                        this.tableData.splice(this.idx, 1);
                        this.$message.success('删除成功');
                        this.delVisible = false;
                        this.search();
                    } else {
                        this.$message.error(res.data.msg);
                        this.delVisible = false;
                    }
                }).catch(function (error) {
                    this.$message.success('删除失败');
                    alert("err==" + error);
                    this.delVisible = false;
                });

            },
            //接收新增
            acceptAdd() {
                this.addLoadingBtn = true
                //先判断选中状态下是否包含子菜单  包含就都存   不包含 单存一个
                //判断半选中状态的  一定包含子菜单  都存上
                //回显时只回显最下级菜单就可以的
                if (this.formAdd.add_role_name === null || this.formAdd.add_role_name === '' || this.formAdd.add_role_name === undefined || this.formAdd.add_role_name === 'undefined') {
                    this.$message.error('角色名称不能为空');
                    this.addLoadingBtn = false
                    return false;
                }
                let menu_id = this.$refs.add_tree.getCheckedKeys();//选中的
                let menu_id_half = this.$refs.add_tree.getHalfCheckedKeys();//半选中的

                let role_json = {
                    menu_id: menu_id,
                    menu_id_half: menu_id_half,
                    role_name: this.formAdd.add_role_name,
                    describe: this.formAdd.add_describe
                }
                this.$axios.post("/api/sys_role/add_role", role_json).then((res) => {
                    if (res.data.code === 200) {
                        this.search()
                        this.$message.success('新增成功');
                        this.addVisible = false;
                        this.addLoadingBtn = false;
                    }
                }).catch(function (error) {
                    this.$message.error(error);
                    this.addLoadingBtn = false
                });
            },

            //id-pid转id,children格式
            toTree(data) {
                let cloneData = JSON.parse(JSON.stringify(data))    // 对源数据深度克隆
                return cloneData.filter(father => {
                    let branchArr = cloneData.filter(child => father.id === child.pid)    //返回每一项的子级数组
                    branchArr.length > 0 ? father.children = branchArr : ''   //如果存在子级，则给父级添加一个children属性，并赋值
                    return father.pid === 0;      //返回第一层
                });
            },

            handleSizeChange(val) {
                this.pageSize = val
                this.search()
            },
            handleCurrentChange(val) {
                this.nowPage = val
                this.search()
            }
        }
    }

</script>

<style scoped>
    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
    }

    .handle-input {
        width: 300px;
        display: inline-block;
    }

    .del-dialog-cnt {
        font-size: 16px;
        text-align: center
    }

    .table {
        width: 100%;
        font-size: 14px;
    }

    .red {
        color: #ff0000;
    }

    .mr10 {
        margin-right: 10px;
    }
</style>
