<template>
    <div class="table">
        <div class="container">
            <div class="handle-box">
                <el-button type="primary" icon="el-icon-plus" @click="add">新增</el-button>
            </div>
            <el-table :data="tableData" border class="table" ref="Table" v-loading="loading" row-key="id" stripe
                      lazy :load="load" @selection-change="chooseInstance">
                <el-table-column type="selection" width="55" align="center"></el-table-column>
                <el-table-column prop="menu_name" label="菜单名称" width="150" align="center">
                </el-table-column>
                <el-table-column prop="url" label="访问地址" width="120" align="center">
                </el-table-column>
                <el-table-column prop="icon" label="图标" align="center" :formatter="formattericon">
                </el-table-column>
                <el-table-column prop="order" label="排序" align="center">
                </el-table-column>
                <el-table-column prop="type" label="类型" align="center" :formatter="formattertype">
                </el-table-column>
                <el-table-column prop="create_time" label="创建时间" align="center">
                </el-table-column>
                <el-table-column prop="update_time" label="最后更新时间" align="center">
                </el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
<!--                        <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑-->
<!--                        </el-button>-->
                        <el-button type="text" icon="el-icon-delete" class="red"
                                   @click="handleDelete(scope.$index, scope.row)">删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="40%" v-loading="updateLoading">
            <el-form ref="form" :model="form" label-width="120px">
                <el-form-item label="登录名">
                    <el-input v-model="form.update_name" disabled></el-input>
                    <el-input v-model="form.update_id" disabled></el-input>
                    <el-input v-model="form.update_role_id" disabled></el-input>
                </el-form-item>
                <el-form-item label="邮箱">
                    <el-input v-model="form.update_email"></el-input>
                </el-form-item>
                <el-form-item label="联系方式">
                    <el-input v-model="form.update_mobile"></el-input>
                </el-form-item>
                <el-form-item label="角色">
                    <el-select v-model="form.update_role_id" placeholder="角色">
                        <el-option v-for="item in role_list" :key="item.id" :label="item.name" :value="item.id">
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

        <!-- 菜单没有父级提示 -->
        <el-dialog title="提示" :visible.sync="isFirst" width="300px" center>
            <div class="del-dialog-cnt">该菜单没有父级菜单,是否继续添加？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="isFirst = false">取 消</el-button>
                <el-button type="primary" @click="add_page">确 定</el-button>
            </span>
        </el-dialog>


        <!-- 修改弹出框 -->
        <el-dialog title="修改菜单" :visible.sync="addVisible" width="40%" v-loading="addLoading">
            <el-dialog width="30%" title="请选择图标" :visible.sync="iconVisible" append-to-body>
                <p class="example-p" v-for="icon in list_icon">{{icon.name}}1111
                    <el-tooltip class="item" effect="dark" :content="icon.name" placement="top-start">
                        <i :class="icon.address" style="font-size: 30px;color: #ff5900"></i>
                    </el-tooltip>
                </p>
            </el-dialog>

            <el-form ref="form" :model="formAdd" label-width="120px">
                <el-form-item label="菜单名称">
                    <el-input v-model="formAdd.add_name"></el-input>
                </el-form-item>
                <el-form-item label="访问地址URL">
                    <el-input v-model="formAdd.add_url"></el-input>
                </el-form-item>
                <el-form-item label="图标">
                    <el-input v-model="formAdd.add_icon" readonly suffix-icon="el-icon-search"
                              @click.native="choose_icon" prefix-icon=icon_data></el-input>
                </el-form-item>
                <el-form-item label="排序">
                    <el-input v-model="formAdd.add_order"></el-input>
                </el-form-item>
                <el-form-item label="类别">
                    <el-radio v-model="formAdd.add_type" label="1">菜单</el-radio>
                    <el-radio v-model="formAdd.add_type" label="2">按钮</el-radio>
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
    // import data from './icon.json'

    export default {
        name: 'basetable',
        data() {
            return {
                list_icon: [{
                    "name": "信息",
                    "address": "el-icon-info"
                },
                    {
                        "name": "错误",
                        "address": "el-icon-error"
                    },
                    {
                        "name": "成功",
                        "address": "el-icon-success"
                    },
                    {
                        "name": "警告",
                        "address": "el-icon-warning"
                    }],
                icon_data: '',
                choose_id: '',
                hideRow: '',
                is_search: false,
                role_list: [],
                tableData: [],
                select_word: '',
                editVisible: false,
                addVisible: false,
                delVisible: false,
                isFirst: false,
                loading: true,
                addLoading: false,
                updateLoading: false,
                iconVisible: false,
                checkAdd: 0,
                delId: '',
                radioVal: 1,
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
                    add_url: '',
                    add_icon: '',
                    add_order: '',
                    add_type: ''
                },
            }
        },

        created() {
            let json = {}
            this.$axios.post("/api/sys_menu/get_menu_list", json).then((res) => {
                this.tableData = res.data.data
                this.loading = false
            }).catch(function (error) {
                this.loading = false
                console.log("err==" + error);
            });
        },
        methods: {
            chooseInstance(val) {
                this.choose_id = val
                if (val.length > 1) {
                    this.$refs.Table.clearSelection()
                    this.$refs.Table.toggleRowSelection(val.pop())
                } else {

                }
            },

            load(tree, treeNode, resolve) {
                this.loading = true
                let json = {menu_id: tree.id}
                this.$axios.post("/api/sys_menu/get_next_menu_list", json).then((res) => {
                    resolve(res.data.data)
                    this.loading = false
                }).catch(function (error) {
                    this.loading = false
                    console.log("err==" + error);
                });
            },

            formattericon(row) {
                return row.icon
            },
            formattertype(row) {
                if (row.type === 1) {
                    return "菜单"
                } else if (row.type === 2) {
                    return "按钮"
                } else {
                    return "其它"
                }
            },
            search() {
                this.loading = true
                let json = {}
                this.$axios.post("/api/sys_menu/get_menu_list", json).then((res) => {
                    this.tableData = res.data.data
                    this.loading = false
                }).catch(function (error) {
                    this.loading = false
                    console.log("err==" + error);
                });
            },
            //新增弹出层
            add() {
                if (this.choose_id === null || this.choose_id === "" || this.choose_id === "undefined" || this.choose_id === undefined || this.choose_id.length < 1) {
                    this.isFirst = true
                } else {
                    if (this.choose_id[0].type === 2) {
                        this.$message.error("按钮下,不允许再添加任何子(菜单/按钮)")
                        return false
                    }
                    this.add_page()
                }
            },
            choose_icon() {
                this.iconVisible = true
            },
            add_page() {
                this.isFirst = false
                this.addLoading = true
                this.formAdd = {
                    add_name: '',
                    add_url: '',
                    add_icon: '',
                    add_order: '',
                    add_type: '1'
                }
                this.addVisible = true;
                this.addLoading = false
            },

            handleEdit(index, row) {
                this.form = {
                    update_id: row.id,
                    update_name: row.username,
                    update_email: row.email,
                    update_mobile: row.mobile,
                    update_role_id: row.role_id,
                    // update_role_id: '13',
                    update_role_name: row.mobile,
                };
                this.editVisible = true;
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
                let json = {menu_id: this.delId};
                this.$axios.post("/api/sys_menu/del_menu", json).then((res) => {
                    if (res.data.code == '200' || res.data.code == 200) {
                        this.tableData.splice(this.idx, 1);
                        this.$message.success('删除成功');
                        this.delVisible = false;
                    } else if (res.data.code == '203' || res.data.code == 203) {
                        this.$message.error(res.data.msg);
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
                if (this.formAdd.add_name === null || this.formAdd.add_name === "" || this.formAdd.add_name === undefined || this.formAdd.add_name === "undefined") {
                    this.$message.error('菜单名不能为空');
                    return false
                }

                if (this.formAdd.add_url === null || this.formAdd.add_url === "" || this.formAdd.add_url === undefined || this.formAdd.add_url === "undefined") {
                    this.$message.error('访问地址不能为空');
                    return false
                }

                if (this.formAdd.add_type === null || this.formAdd.add_type === "" || this.formAdd.add_type === undefined || this.formAdd.add_type === "undefined") {
                    this.$message.error('类别不能为空');
                    return false
                }

                this.addLoading = true
                let menu_json = {
                    add_name: this.formAdd.add_name,
                    add_url: this.formAdd.add_url,
                    add_icon: this.formAdd.add_icon,
                    add_order: this.formAdd.add_order,
                    add_type: this.formAdd.add_type,
                }

                if (this.choose_id !== null && this.choose_id !== "" && this.choose_id !== "undefined" && this.choose_id !== undefined) {
                    alert(1)
                    menu_json.pid = this.choose_id[0].id
                }

                this.$axios.post("/api/sys_menu/add_menu", menu_json).then((res) => {
                    if (res.data.code === 200) {
                        this.addLoading = false
                        this.search()
                        this.$message.success('新增成功');
                        this.addVisible = false;
                    } else if (res.data.code === 203) {
                        this.$message.error(res.data.msg);
                    } else {
                        alert(res.data.msg)
                    }
                }).catch(function (error) {
                    alert(error)
                    this.addLoading = false
                });
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

    /*去掉表头的复选按钮,将表格设置为单选*/
    .el-table--enable-row-transition >>> thead .el-table-column--selection .cell {
        display: none;
    }
</style>
