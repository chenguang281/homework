<template>
    <div class="">
        <div class="container">
            <el-tabs v-model="table_code" type="card" :before-leave="add_table" @v-for="tab_data"
                     v-loading="tab_loading">
                <el-tab-pane :label="module.table_comment" :name="module.table_code" v-for="module in tab_data"
                             :key="module.table_code">
                </el-tab-pane>
                <el-tab-pane key="addButton">
                   <span slot="label" style="padding: 8px" @click="add_table_span">
                     <i class="el-icon-plus"></i>
                   </span>
                </el-tab-pane>
                <div class="handle-box">
                    <el-input v-model="column_select_name" placeholder="筛选关键词" class="handle-input mr10"
                              clearable></el-input>
                    <el-button type="primary" icon="el-icon-search" @click="column_search" @keyup.enter="column_search">
                        搜索
                    </el-button>
                    <el-button type="primary" icon="el-icon-plus" @click="add_column_dicts">新增</el-button>
                </div>
                <el-table :data="column_table_data" border class="table" ref="multipleTable"
                          v-loading="column_loading">
                    <el-table-column prop="column_code" label="对应列名" width="250" align="center" sortable>
                    </el-table-column>
                    <el-table-column prop="column_comment" label="对应列备注" width="250" align="center" sortable>
                    </el-table-column>
                    <el-table-column prop="name" label="回调显示" width="300" align="center" sortable>
                    </el-table-column>
                    <el-table-column prop="num" label="存储值" align="center" sortable>
                    </el-table-column>
                    <el-table-column prop="value" label="真实值(部分计算代替值)" align="center" sortable>
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
                        @size-change="handleSizeChange_column"
                        @current-change="handleCurrentChange_column"
                        :current-page="nowPage_column"
                        :page-sizes=pageSizeArr_column
                        :page-size=pageSize_column
                        layout="total, sizes, prev, pager, next, jumper"
                        :total=total_column
                        class="pagination">
                </el-pagination>
            </el-tabs>
        </div>

        <!-- 新增列弹出框 -->
        <el-dialog :title="titleName" :visible.sync="column_add_page" width="40%" v-loading="column_add_loading"
                   top="5vh">
            <el-form ref="column_form" :model="column_add" label-width="120px">
                <el-form-item label="对应列">
                    <el-select v-model="column_add.column_code" placeholder="-请选择-" clearable>
                        <el-option v-for="item in column_code_list" :key="item.column_comment"
                                   :label="item.column_comment"
                                   :value="item.column_name">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="存储值">
                    <el-input v-model="column_add.save_value"></el-input>
                </el-form-item>
                <el-form-item label="回调显示">
                    <el-input v-model="column_add.callback_value"></el-input>
                </el-form-item>
                <el-form-item label="真实值">
                    <el-input v-model="column_add.real_value"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="column_add_page = false">取 消</el-button>
                <el-button type="primary" @click="column_add_submit">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 新增tab弹出框（表操作） -->
        <el-dialog title="新增字典" :visible.sync="table_add_page" width="40%" v-loading="table_add_loading" top="5vh" >
            <el-form :model="column_add">
                <div class="handle-box">
                    <el-input v-model="table_select_name" placeholder="筛选关键词" class="handle-input mr10"
                              clearable></el-input>
                    <el-button type="primary" icon="el-icon-search" @click="table_search" @keyup.enter="table_search">
                        搜索
                    </el-button>
                </div>
                <el-table :data="table_data" border class="table_table" ref="Table_ref"
                          @selection-change="chooseInstance">
                    <el-table-column type="selection" width="55" align="center"></el-table-column>
                    <el-table-column prop="tableName" label="表名" width="250" align="center" sortable>
                    </el-table-column>
                    <el-table-column prop="realName" label="表注释" width="340" align="center" sortable>
                    </el-table-column>
                </el-table>
                <el-pagination
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange"
                        :current-page="nowPage"
                        :page-size=pageSize
                        layout="total, prev, pager, next, jumper"
                        :total=total
                        class="pagination">
                </el-pagination>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="table_add_page = false">取 消</el-button>
                <el-button type="primary" @click="table_add_submit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: 'tabs',
        data() {
            return {
                tab_data: [], //标签头（表数据）
                column_table_data: [],//列数据
                table_data: [],//表数据


                table_code: '0',//记录当前标签页（区分新增使用）
                column_select_name: '',//列筛选条件
                table_select_name: '',//表筛选条件
                titleName: '',
                tab_loading: true,//记载标签头等待
                column_loading: false,//加载列数据等待
                column_add_loading: true,//新增列字典等待加载表内列
                table_add_loading: true,//新增表字典等待加载表等待

                column_add_page: false,//新增列页面控制参数
                table_add_page: false,//新增表字典控制参数


                //列分页参数
                nowPage_column: 1,//初始化页数--当前页
                total_column: 0, //总条数
                pageSize_column: 10, //初始每页条数
                pageSizeArr_column: [10, 20, 50, 100],//每页展示条数数组


                //表分页参数
                nowPage: 1,//初始化页数--当前页
                total: 0, //总条数
                pageSize: 10, //初始每页条数
                pageSizeArr: [10, 20, 50, 100],//每页展示条数数组

                //新增列传递数据
                column_add: {
                    column_code: '',//对应列
                    save_value: '',//保存值（字典值）
                    callback_value: '',//回显值
                    real_value: '',//真实值（一般不需要填写）
                },
                column_code_list: {},//出去id和varchar字段的下拉列表


                choose_id: '',

            }
        },
        created() {
            //得到所有页签
            this.$axios.post("/api/sys_set/dicts/get_tab").then((res) => {
                if (res.data.data !== null && res.data.data.length > 0) {
                    this.table_code = res.data.data[0].table_code;
                    this.titleName = '新增-' + res.data.data[0].table_comment + '-字典'
                    this.tab_data = res.data.data;
                }
                this.tab_loading = false;
            }).catch(function (error) {
                this.tab_loading = false
            });
        },

        watch: {
            table_code: function () {
                this.column_loading = true
                //清空查询条件
                this.column_select_name = "";
                if (this.table_name !== null && this.table_name !== "") {
                    let json = {
                        table_name: this.table_code,
                        nowPage: this.nowPage,
                        pagesize: this.pageSize
                    }
                    this.$axios.post("/api/sys_set/dicts/get_tab_column", json).then((res) => {
                        this.column_table_data = res.data.data
                        this.nowPage_column = res.data.nowPage
                        this.total_column = res.data.total;
                        this.column_loading = false
                    }).catch(function (error) {
                        this.column_loading = false

                    });
                } else {
                    this.column_loading = false
                }

            },
        },

        methods: {
            //列查询
            column_search() {
                let json = {
                    table_name: this.table_code,
                    select_name: this.column_select_name,
                    nowPage: this.nowPage_column,
                    pagesize: this.pageSize_column
                }
                this.$axios.post("/api/sys_set/dicts/get_tab_column", json).then((res) => {
                    this.column_table_data = res.data.data
                    this.nowPage_column = res.data.nowPage
                    this.total_column = res.data.total;
                    this.column_loading = false
                }).catch(function (error) {
                    this.column_loading = false

                });
            },

            // 新增列弹出
            add_column_dicts() {
                if (this.table_code !== null && this.table_code !== '' && this.table_code !== 0 && this.table_code !== '0') {
                    //弹出之前清理上次值
                    this.column_add.column_code = '',//对应列
                        this.column_add.save_value = '',//保存值（字典值）
                        this.column_add.callback_value = '',//回显值
                        this.column_add.real_value = '',//真实值（一般不需要填写）


                        this.column_add_loading = true
                    let json = {
                        table_name: this.table_code
                    }
                    this.$axios.post("/api/sys_set/dicts/get_column", json).then((res) => {
                        this.column_code_list = res.data.data
                        this.column_add_loading = false
                        this.column_add_page = true
                    }).catch(function (error) {
                        this.column_add_loading = false

                    });
                } else {
                    this.$message.error("没有对应表，请先选择对应表～！");
                }


            },

            //新增列字典保存
            column_add_submit() {
                let json = {
                    column_add: this.column_add,
                    table_code: this.table_code
                }
                this.$axios.post("/api/sys_set/dicts/save_dicts", json).then((res) => {
                    this.column_add_page = false
                    this.column_search()
                }).catch(function (error) {

                });
            },

            //新增表字典弹出---禁止页签切换
            add_table(table_code) {
                if (table_code == this.tab_data.length && this.tab_data.length > 0) {
                    return false
                }
            },
            //新增表字典弹出
            add_table_span() {
                this.table_add_loading = true
                this.table_select_name = ''

                let json = {
                    nowPage: this.nowPage,
                    pagesize: this.pageSize
                }
                this.$axios.post("/api/sys_set/dicts/get_tables", json).then((res) => {
                    this.table_data = res.data.data
                    this.nowPage_column = res.data.nowPage
                    this.total = res.data.total
                    this.table_add_loading = false
                    this.table_add_page = true
                }).catch(function (error) {
                    this.table_add_loading = false
                });
                return false
            },

            //表模糊查询
            table_search() {
                let json = {
                    select_name: this.table_select_name,
                    nowPage: this.nowPage,
                    pagesize: this.pageSize
                }
                this.$axios.post("/api/sys_set/dicts/get_tables", json).then((res) => {
                    this.table_data = res.data.data
                    this.nowPage = res.data.nowPage
                    this.total = res.data.total
                    this.table_add_loading = false
                }).catch(function (error) {
                    this.table_add_loading = false
                });
            },
            //列分页翻页
            handleSizeChange_column(val) {
                this.pageSize_column = val
                this.column_search()
            },
            //列分页翻页
            handleCurrentChange_column(val) {
                this.nowPage_column = val
                this.column_search()
            },
            //表分页翻页
            handleSizeChange(val) {
                this.pageSize = val
                this.table_search()
            },
            //表分页翻页
            handleCurrentChange(val) {
                this.nowPage = val
                this.table_search()
            },
            //新增表保存
            table_add_submit() {
                if (this.choose_id != "" && this.choose_id != null) {
                    this.tab_data_one = {"table_code": this.choose_id[0].realName}
                    this.tab_data_one = {"table_comment": this.choose_id[0].realName}
                    this.tab_data.push(this.tab_data_one)
                    this.table_code = this.choose_id[0].tableName
                    this.titleName = '新增-' + this.choose_id[0].realName + '-字典'
                    this.table_add_page = false
                    this.add_column_dicts()
                }

            },

            // 单选操作
            chooseInstance(val) {
                this.choose_id = val
                if (val.length > 1) {
                    this.$refs.Table_ref.clearSelection()
                    this.$refs.Table_ref.toggleRowSelection(val.pop())
                } else {

                }
            },

            //删除弹出提示
            handleDelete() {

            },
            //编辑弹出层
            handleEdit() {

            },
        },

    }

</script>

<style>

    .handle-input {
        width: 300px;
        display: inline-block;
    }

    .mr10 {
        margin-right: 10px;
        margin-bottom: 15px;
    }

    /*去掉表头的复选按钮,将表格设置为单选*/
    /*.el-dialog__wrapper.abcde >>> .el-dialog .el-dialog__body{*/
    /*    display: none;*/
    /*}*/
    .is-center.el-table-column--selection.is-leaf .cell{
        display: none;
    }
</style>

