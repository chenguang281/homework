<template>
    <div class="sidebar">
        <el-menu class="sidebar-el-menu" :default-active="onRoutes" :collapse="collapse" background-color="#324157"
                 text-color="#bfcbd9" active-text-color="#20a0ff" unique-opened router>
            <template v-for="item in items">
                <template v-if="item.subs">
                    <el-submenu :index="item.url" :key="item.url">
                        <template slot="title">
                            <i :class="item.icon"></i><span slot="title">{{ item.menu_name }}</span>
                        </template>
                        <template v-for="subItem in item.subs">
                            <el-submenu v-if="subItem.subs" :index="subItem.url" :key="subItem.url">
                                <template slot="title">{{ subItem.menu_name }}</template>
                                <el-menu-item v-for="(threeItem,i) in subItem.subs" :key="i" :index="threeItem.url">
                                    {{ threeItem.menu_name }}
                                </el-menu-item>
                            </el-submenu>
                            <el-menu-item v-else :index="subItem.url" :key="subItem.url">
                                {{ subItem.menu_name }}
                            </el-menu-item>
                        </template>
                    </el-submenu>
                </template>
                <template v-else>
                    <el-menu-item :index="item.url" :key="item.url">
                        <i :class="item.icon"></i><span slot="title">{{ item.menu_name }}</span>
                    </el-menu-item>
                </template>
            </template>
        </el-menu>
    </div>
</template>

<script>
    import bus from '../common/bus';


    export default {
        data() {
            return {
                collapse: false,
                items: [

                ]
            }
        },
        computed: {
            onRoutes() {
                return this.$route.path.replace('/', '');
            }
        },
        created() {
            // 通过 Event Bus 进行组件间通信，来折叠侧边栏

            let user_id = {user_id: sessionStorage.getItem('user_id')}
            this.$axios.post("/api/sys_user/get_permission", user_id).then((res) => {
                this.items = this.toTree(res.data.data);
            }).catch(function (error) {
                console.log("err==" + error);
            });

            bus.$on('collapse', msg => {
                this.collapse = msg;
            })
        },
        methods: {
            toTree(data) {
                let cloneData = JSON.parse(JSON.stringify(data))    // 对源数据深度克隆
                return cloneData.filter(father => {
                    let branchArr = cloneData.filter(child => father.id === child.pid)    //返回每一项的子级数组
                    branchArr.length > 0 ? father.subs = branchArr : ''   //如果存在子级，则给父级添加一个children属性，并赋值
                    return father.pid === 0;      //返回第一层
                });
            }
        }
    }
</script>

<style scoped>
    .sidebar {
        display: block;
        position: absolute;
        left: 0;
        top: 70px;
        bottom: 0;
        overflow-y: scroll;
    }

    .sidebar::-webkit-scrollbar {
        width: 0;
    }

    .sidebar-el-menu:not(.el-menu--collapse) {
        width: 250px;
    }

    .sidebar > ul {
        height: 100%;
    }
</style>
