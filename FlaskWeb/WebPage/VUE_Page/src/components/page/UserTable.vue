<template>
    <div class="table">
        <div class="container">
            <div class="handle-box">
                <el-input v-model="select_word" placeholder="筛选关键词" class="handle-input mr10" clearable></el-input>
                <el-button type="primary" icon="el-icon-search" @click="search" @keyup.enter="search">搜索</el-button>
                <el-button type="primary" icon="el-icon-plus" @click="add">新增</el-button>
            </div>
            <el-table :data="tableData" border class="table" ref="multipleTable" v-loading="loading">
                <el-table-column prop="username" label="用户名" width="150" align="center" sortable>
                </el-table-column>
                <el-table-column prop="email" label="邮箱" width="120" align="center" sortable>
                </el-table-column>
                <el-table-column prop="mobile" label="联系方式" align="center" sortable>
                </el-table-column>
                <el-table-column prop="role_name" label="角色名称" align="center" sortable>
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
        <el-dialog title="编辑" :visible.sync="editVisible" width="40%" v-loading="updateLoading">
            <el-form ref="form" :model="form" label-width="120px">
                <el-form-item label="登录名">
                    <el-input v-model="form.update_name" disabled></el-input>
                </el-form-item>
                <el-form-item label="邮箱">
                    <el-input v-model="form.update_email"></el-input>
                </el-form-item>
                <el-form-item label="联系方式">
                    <el-input v-model="form.update_mobile"></el-input>
                </el-form-item>
                <el-form-item label="角色">
                    <el-select v-model="form.update_role_id" placeholder="角色">
                        <el-option v-for="item in role_list" :key="item.id" :label="item.role_name" :value="item.id">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
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
        <el-dialog title="新增用户" :visible.sync="addVisible" width="40%" v-loading="addLoading">
            <el-form ref="form" :column_add="formAdd" label-width="120px">
                <el-form-item label="登录名">
                    <el-input v-model="formAdd.add_name"></el-input>
                </el-form-item>
                <el-form-item label="密码">
                    <el-input type="password" v-model="formAdd.add_password"></el-input>
                </el-form-item>
                <el-form-item label="确认密码">
                    <el-input type="password" v-model="formAdd.add_password_check"></el-input>
                </el-form-item>
                <el-form-item label="邮箱">
                    <el-input v-model="formAdd.add_email"></el-input>
                </el-form-item>
                <el-form-item label="联系方式">
                    <el-input v-model="formAdd.add_mobile"></el-input>
                </el-form-item>
                <el-form-item label="角色">
                    <el-select v-model="formAdd.add_role_id" placeholder="角色">
                        <el-option v-for="item in role_list" :key="item.id" :label="item.role_name" :value="item.id">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addVisible = false">取 消</el-button>
                <el-button type="primary" @click="acceptAdd">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: 'usertable',
        data() {
            return {
                nowPage: 1,//初始化页数--当前页
                total: 0, //总条数
                pageSize: 10, //初始每页条数
                pageSizeArr: [10, 20, 50, 100],//每页展示条数数组

                value: true,
                hideRow: '',
                is_search: false,
                role_list: [],
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
                form: {
                    update_id: '',
                    update_name: '',
                    update_email: '',
                    update_mobile: '',
                    update_role_id: '',
                    update_role_name: '',
                },
                //新增传递数据
                formAdd: {
                    add_name: '',
                    add_email: '',
                    add_mobile: '',
                    add_role_id: '',
                    add_password: '',
                    add_password_check: ''
                },
            }
        },
        created() {
            let json = {
                nowPage: this.nowPage,
                pagesize: this.pageSize
            }
            this.$axios.post("/api/sys_user/get_user_list", json).then((res) => {
                this.loading = false
                if (res.data.code === 200 || res.data.code === "200") {
                    this.tableData = res.data.data
                    this.total = res.data.total;

                } else {
                    this.$message.error(res.data.msg);
                }
            }).catch(function (error) {
                this.loading = false
                console.log("err==" + error);
            });
        },
        methods: {
            //条件查询
            search() {
                this.loading = true
                let json = {
                    user_name: this.select_word,
                    nowPage: this.nowPage,
                    pagesize: this.pageSize
                }
                this.$axios.post("/api/sys_user/get_user_list", json).then((res) => {
                    this.tableData = res.data.data
                    this.nowPage = res.data.nowPage
                    this.total = res.data.total;
                    this.loading = false
                }).catch(function (error) {
                    this.loading = false
                    console.log("err==" + error);
                });
            },
            //新增弹出层
            add() {
                this.addLoading = true
                this.formAdd = {
                    add_name: '',
                    add_email: '',
                    add_mobile: '',
                    add_role_id: ''
                }
                let role_json = {}
                this.$axios.post("/api/sys_role/get_role_list", role_json).then((res) => {
                    this.role_list = res.data.data
                    this.addVisible = true
                    this.addLoading = false
                }).catch(function (error) {
                    alert(error)
                    alert('拉去角色失败,请重新尝试')
                    this.addLoading = false
                })
            },

            handleEdit(index, row) {
                this.form = {
                    update_id: row.id,
                    update_name: row.username,
                    update_email: row.email,
                    update_mobile: row.mobile,
                    update_role_id: row.role_id,
                    update_role_name: row.mobile,
                }
                let role_json = {}
                this.$axios.post("/api/sys_role/get_role_list", role_json).then((res) => {
                    this.role_list = res.data.data
                    this.editVisible = true;
                }).catch(function (error) {
                    this.$message.error('拉取角色失败,请重新尝试')
                })
            },

            // 保存编辑
            saveEdit() {
                this.updateLoading = true
                let json = {}
                json.id = this.form.update_id
                json.email = this.form.update_email
                json.mobile = this.form.update_mobile
                json.role_id = this.form.update_role_id
                this.$axios.post("/api/sys_user/update_user", json).then((res) => {
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
                let json = {user_id: this.delId};
                this.$axios.post("/api/sys_user/del_user", json).then((res) => {
                    if (res.data.code == '200' || res.data.code == 200) {
                        this.tableData.splice(this.idx, 1);
                        this.$message.success('删除成功');
                        this.delVisible = false;
                    } else {
                        this.$message.error('删除失败');
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
                this.addLoading = true;
                if (this.formAdd.add_name === null || this.formAdd.add_name === "" || this.formAdd.add_name === undefined || this.formAdd.add_name === "undefined") {
                    this.$message.error('用户名不能为空');
                    this.addLoading = false;
                    return false
                }
                if (this.formAdd.add_password === null || this.formAdd.add_password === "" || this.formAdd.add_password === undefined || this.formAdd.add_password === "undefined") {
                    this.$message.error('密码不能为空');
                    this.addLoading = false;
                    return false
                }

                if (this.formAdd.add_password !== this.formAdd.add_password_check) {
                    this.$message.error('两次密码不一致');
                    this.addLoading = false;
                    return false
                }
                let user_json = {
                    username: this.formAdd.add_name,
                    password: this.formAdd.add_password,
                    passwordCheck: this.formAdd.add_password_check,
                    email: this.formAdd.add_email,
                    mobile: this.formAdd.add_mobile,
                    role_id: this.formAdd.add_role_id,
                }
                this.$axios.post("/api/sys_user/add_user", user_json).then((res) => {
                    this.addLoading = false;
                    if (res.data.code === 200) {
                        this.search()
                        this.$message.success('新增成功');
                        this.addVisible = false;
                    } else {
                        this.$message.error(res.data.msg);
                    }
                }).catch(function (error) {

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
