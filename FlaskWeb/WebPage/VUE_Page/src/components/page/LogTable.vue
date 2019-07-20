<template>
    <div class="table">
        <div class="container">
            <div class="handle-box">
                <el-input v-model="select_word" placeholder="筛选关键词" class="handle-input mr10" clearable></el-input>
                <span class="font-size-color">登录时间：</span>
                <el-date-picker
                        v-model="select_create_time"
                        type="daterange"
                        align="right"
                        value-format="yyyy-MM-dd"
                        unlink-panels
                        range-separator="至"
                        start-placeholder="开始日期"
                        end-placeholder="结束日期"
                        :picker-options="pickerOptions">
                </el-date-picker>
                &nbsp;
                <span class="font-size-color">是否成功：</span>
                <el-select v-model="select_status" class="handle-select mr10" style="color: #999;">
                    <el-option label="全部" value=""></el-option>
                    <el-option label="登录成功" value="1"></el-option>
                    <el-option label="登录失败" value="0"></el-option>
                </el-select>
                <el-button type="primary" icon="el-icon-search" @click="search">搜索</el-button>
            </div>
            <el-table :data="tableData" border class="table" ref="multipleTable" v-loading="loading"
                      :default-sort="{prop: 'create_time', order: 'descending'}">
                <el-table-column prop="username" label="用户ID" width="150" align="center" sortable>
                </el-table-column>
                <el-table-column prop="status" label="是否成功" width="150" align="center" sortable>
                </el-table-column>
                <el-table-column prop="ip" label="登录IP" align="center" width="180" sortable>
                </el-table-column>
                <el-table-column prop="token" label="token" align="center" sortable>
                </el-table-column>
                <el-table-column prop="create_time" label="登录时间" align="center" sortable>
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
    </div>
</template>

<script>
    export default {
        name: 'logtable',
        data() {
            return {
                nowPage: 1,//初始化页数--当前页
                total: 0, //总条数
                pageSize: 10, //初始每页条数
                pageSizeArr: [10, 20, 50, 100],//每页展示条数数组


                pickerOptions: {
                    shortcuts: [{
                        text: '最近一周',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                            picker.$emit('pick', [start, end]);
                        }
                    }, {
                        text: '最近一个月',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                            picker.$emit('pick', [start, end]);
                        }
                    }, {
                        text: '最近三个月',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                            picker.$emit('pick', [start, end]);
                        }
                    }]
                },
                select_status: '1',
                tableData: [],
                select_word: '',
                select_create_time: '',
                loading: true,
            }
        },
        created() {
            let json = {
                nowPage: this.nowPage,
                pagesize: this.pageSize,
                select_status:1
            }
            this.$axios.post("/api/sys_log/get_all", json).then((res) => {
                this.tableData = res.data.data
                this.total = res.data.total
                this.loading = false
            }).catch(function (error) {
                this.loading = false
                console.log("err==" + error);
            });
        },
        methods: {
            search() {
                this.loading = true
                let json = {
                    select_word: this.select_word,
                    select_create_time: this.select_create_time,
                    select_status: this.select_status,
                    nowPage: this.nowPage,
                    pagesize: this.pageSize
                }
                this.$axios.post("/api/sys_log/get_all", json).then((res) => {
                    this.tableData = res.data.data
                    this.total = res.data.total
                    this.nowPage = res.data.nowPage
                    this.loading = false
                }).catch(function (error) {
                    this.loading = false
                    console.log("err==" + error);
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

    .font-size-color {
        font-size: 14px;
        color: #999;
        line-height: 25px;
    }

    .handle-input {
        width: 200px;
        display: inline-block;
    }

    .table {
        width: 100%;
        font-size: 14px;
    }

    .mr10 {
        margin-right: 10px;
    }

    .pagination {
        margin-left: 10%;
    }
</style>
