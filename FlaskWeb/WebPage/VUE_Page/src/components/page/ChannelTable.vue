<template>
    <div class="table">
        <div class="container">
            <div class="handle-box">
                <el-input v-model="select_word" placeholder="筛选关键词" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="search">搜索</el-button>
                <el-button type="primary" icon="el-icon-plus" @click="add">新增</el-button>
            </div>
            <el-table :data="tableData" border class="table" ref="multipleTable" v-loading="loading">
                <el-table-column type="expand">
                    <template slot-scope="props">
                        <el-form label-position="left" inline class="table-expand">
                            <el-form-item label="渠道名称">
                                <span>{{ props.row.channelName }}</span>
                            </el-form-item>
                            <el-form-item label="渠道地址">
                                <span>{{ props.row.address }}</span>
                            </el-form-item>
                            <el-form-item label="联系方式">
                                <span>{{ props.row.telphone }}</span>
                            </el-form-item>
                            <el-form-item label="移动电话">
                                <span>{{ props.row.mobilePhone }}</span>
                            </el-form-item>
                            <el-form-item label="创建时间">
                                <span>{{ props.row.create_time }}</span>
                            </el-form-item>
                            <el-form-item label="创建人">
                                <span>{{ props.row.username }}</span>
                            </el-form-item>
                            <el-form-item label="最后更新时间">
                                <span>{{ props.row.update_time }}</span>
                            </el-form-item>
                            <el-form-item label="">
                                <span></span>
                            </el-form-item>
                            <el-form-item label="详细地址">
                                <span>{{ props.row.detailed_address }}</span>
                            </el-form-item>
                        </el-form>
                    </template>
                </el-table-column>
                <el-table-column prop="channelName" label="渠道名称" width="480" align="center">
                </el-table-column>
                <el-table-column prop="address" label="渠道地址" width="300" align="center">
                </el-table-column>
                <el-table-column prop="telphone" label="联系方式" align="center">
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
        </div>
        <!-- 删除提示框 -->
        <el-dialog title="提示" :visible.sync="delVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteRow">确 定</el-button>
            </span>
        </el-dialog>

        <!--新增弹出-->
        <el-dialog title="新增" :visible.sync="add_channel" width="50%" v-loading="addLoading">
            <el-form ref="form" :model="add_form" label-width="120px">
                <el-form-item label="渠道名称">
                    <el-input v-model="add_form.channelName" class="add_input"></el-input>
                </el-form-item>
                <el-form-item label="联系方式">
                    <el-input v-model="add_form.telphone" class="add_input"></el-input>
                </el-form-item>
                <el-form-item label="移动电话">
                    <el-input v-model="add_form.mobilePhone" class="add_input"></el-input>
                </el-form-item>
                <el-form-item label="地址">
                    <el-cascader :options="options" v-model="add_form.address"
                                 :disabled="add_form.country"></el-cascader>
                    <el-switch class="add_switch"
                               v-model="add_form.country"
                               active-color="#ff4949"
                               inactive-color="#13ce66"
                               active-text="海外"
                               :active-value="true"
                               inactive-text="国内"
                               :inactive-value="false"
                               @change="change_country">
                    </el-switch>
                </el-form-item>
                <el-form-item label="详细地址">
                    <el-input type="textarea" rows="5" v-model="add_form.detailed_address" class="add_input"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveAdd">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: 'usertable',
        data() {
            return {
                options: [
                    {
                        value: 'guangdong',
                        label: '广东省',
                        children: [
                            {
                                value: 'guangzhou',
                                label: '广州市',
                                children: [
                                    {
                                        value: 'tianhe',
                                        label: '天河区'
                                    },
                                    {
                                        value: 'haizhu',
                                        label: '海珠区'
                                    }
                                ]
                            },
                            {
                                value: 'dongguan',
                                label: '东莞市',
                                children: [
                                    {
                                        value: 'changan',
                                        label: '长安镇'
                                    },
                                    {
                                        value: 'humen',
                                        label: '虎门镇'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        value: 'hunan',
                        label: '湖南省',
                        children: [
                            {
                                value: 'changsha',
                                label: '长沙市',
                                children: [
                                    {
                                        value: 'yuelu',
                                        label: '岳麓区'
                                    }
                                ]
                            }
                        ]
                    }
                ],


                tableData: [],
                loading: true,
                delId: '',
                delVisible: false,
                //新增所需参数
                add_channel: false,
                addLoading: false,
                add_form: {
                    channelName: '',
                    telphone: '',
                    mobilePhone: '',
                    detailed_address: '',
                    address: '',
                    country: false
                },
                city: false,

                select_word: '',
            }
        },
        created() {
            let json = {}
            this.$axios.post("/api/goods/channel/get_all", json).then((res) => {
                this.loading = false
                if (res.data.code === 200 || res.data.code === "200") {
                    this.tableData = res.data.data
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
                let json = {}
                this.$axios.post("/api/goods/channel/get_all", json).then((res) => {
                    this.loading = false
                    if (res.data.code === 200 || res.data.code === "200") {
                        this.tableData = res.data.data
                    } else {
                        this.$message.error(res.data.msg);
                    }
                }).catch(function (error) {
                    this.loading = false
                    console.log("err==" + error);
                });
            },

            //新增弹出层
            add() {
                this.addLoading = true
                this.add_form = {
                    channelName: '',
                    telphone: '',
                    mobilePhone: '',
                    country: false,
                    address: '',
                }
                this.add_channel = true;
                this.addLoading = false
            },
            change_country() {
                console.log(this.add_form.country)

            },
            saveAdd() {
                this.addLoading = true;
                if (this.add_form.channelName === null || this.add_form.channelName === "" || this.add_form.channelName === undefined || this.add_form.channelName === "undefined") {
                    this.$message.error('渠道名称不能为空');
                    this.addLoading = false;
                    return false
                }
                if (this.add_form.telphone === null || this.add_form.telphone === "" || this.add_form.telphone === undefined || this.add_form.telphone === "undefined") {
                    this.$message.error('联系方式不能为空');
                    this.addLoading = false;
                    return false
                }
                if (this.add_form.mobilePhone === null || this.add_form.mobilePhone === "" || this.add_form.mobilePhone === undefined || this.add_form.mobilePhone === "undefined") {
                    this.$message.error('移动电话不能为空');
                    this.addLoading = false;
                    return false
                }
                if (!this.add_form.country) {
                    if (this.add_form.address === null || this.add_form.address === "" || this.add_form.address === undefined || this.add_form.address === "undefined") {
                        this.$message.error('请选择地址');
                        this.addLoading = false;
                        return false
                    }
                }

                if (this.add_form.detailed_address === null || this.add_form.detailed_address === "" || this.add_form.detailed_address === undefined || this.add_form.detailed_address === "undefined") {
                    this.$message.error('移动电话不能为空');
                    this.addLoading = false;
                    return false
                }
                let json = {
                    channelName: this.add_form.channelName,
                    country: this.add_form.country,
                    address: this.add_form.address,
                    telphone: this.add_form.telphone,
                    mobilePhone: this.add_form.mobilePhone,
                    detailed_address: this.add_form.detailed_address
                }
                //开始保存
                this.$axios.post("/api/goods/channel/add_channel", json).then((res) => {
                    this.addLoading = false
                    this.add_channel = false
                    this.search()
                }).catch(function (error) {
                    this.addLoading = false
                    this.add_channel = false
                    console.log("err==" + error);
                });


            },
            deleteRow() {
                alert("删除行数据")
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

    .add_input {
        width: 80%;
    }

    .add_switch {
        margin-left: 60px;
    }

    .table-expand {
        font-size: 0;
    }

    .table-expand>>>label {
        width: 120px;
        color: #99a9bf;
    }

    .table-expand>>>.el-form-item {
        margin-right: 0;
        margin-bottom: 0;
        width: 50%;
    }
</style>
