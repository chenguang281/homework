/*
Navicat MySQL Data Transfer

Source Server         : 本地
Source Server Version : 50641
Source Host           : localhost:3306
Source Database       : flask

Target Server Type    : MYSQL
Target Server Version : 50641
File Encoding         : 65001

Date: 2019-04-23 10:18:40
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for sys_dictionary
-- ----------------------------
DROP TABLE IF EXISTS `sys_dictionary`;
CREATE TABLE `sys_dictionary` (
  `id` varchar(32) NOT NULL COMMENT '主键ID',
  `num` int(11) DEFAULT NULL COMMENT '编码',
  `table_code` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '表名',
  `column_code` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '列名',
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '显示名称',
  `value` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '实际值',
  PRIMARY KEY (`id`),
  KEY `table_code` (`table_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='SYS系统字典表';

-- ----------------------------
-- Records of sys_dictionary
-- ----------------------------
INSERT INTO `sys_dictionary` VALUES ('0275d3668e424690bc4eb907a360f812', '7', 'pro_project', 'application_type', '通信控制', '1.9');
INSERT INTO `sys_dictionary` VALUES ('098498d05a504af184b20d6ee413718f', '6', 'pro_project', 'application_type', '系统', '1.7');
INSERT INTO `sys_dictionary` VALUES ('12648f9434ad49389e818f9d3cdc1a2b', '2', 'pro_project', 'development_language', 'PowerBuilder、ASP及其他同级别语言/平台', '0.6');
INSERT INTO `sys_dictionary` VALUES ('153464e991f34d68a40b653db4ad796d', '1', 'pro_project', 'application_type', '业务处理', '1');
INSERT INTO `sys_dictionary` VALUES ('19bf2e7a1a8f4275ab6f3d29390e5774', '1', 'pro_project', 'distributed_handle', '通过网络进行客户端/服务器及网络基础应用分布处理和传输', '0');
INSERT INTO `sys_dictionary` VALUES ('1d8d8387a0124a47a9988fc3c08bf89b', '3', 'pro_project', 'opportunity', '项目完成(项目开发完成)', '1.00');
INSERT INTO `sys_dictionary` VALUES ('215091fd97034a939eee4031be588fdc', '2', 'pro_project', 'team_background', '为本行业开发过类似的软件', '0.8');
INSERT INTO `sys_dictionary` VALUES ('233a48d8643742e5b25ea248bc8d8888', '2', 'pro_project', 'multiple_sites', '在相同的硬件或软件环境下运行', '1');
INSERT INTO `sys_dictionary` VALUES ('2daace3557af4c59a69932de60e0699f', '2', 'pro_project', 'application_type', '应用集成', '1');
INSERT INTO `sys_dictionary` VALUES ('33ec3610cc7b4d7baf0f98acfca4f433', '2', 'pro_project', 'reliability', '没有明示对可靠性的特别需求事项或仅需提供基本的可靠性', '1');
INSERT INTO `sys_dictionary` VALUES ('44d9d8d5af84488f8b907852c84823ac', '2', 'pro_project', 'distributed_handle', '没有明示对分布式处理的需求事项', '1');
INSERT INTO `sys_dictionary` VALUES ('4b5e50ea32fb416abe3e34a21e1b5050', '3', 'pro_project', 'distributed_handle', '通过特别的设计保证在多个服务器及处理器上同时相互执行应用中的处理功能', '-1');
INSERT INTO `sys_dictionary` VALUES ('59f304e5512f49f9b28dda3c301859ee', '2', 'pro_project', 'demand_grade', 'B', '1.26');
INSERT INTO `sys_dictionary` VALUES ('60dd8757a0254057a524bb7e3982cd24', '3', 'pro_project', 'demand_grade', 'C', '1.00');
INSERT INTO `sys_dictionary` VALUES ('642f4a35aa704ea89eea14f65681b463', '3', 'pro_project', 'multiple_sites', '在设计阶段需要考虑不同站点的不同硬件或软件环境下运行需求', '-1');
INSERT INTO `sys_dictionary` VALUES ('6ab18c1df90c44919e0ec771f9ef12f1', '1', 'pro_project', 'performance', '应答时间或处理率对高峰时间或所有业务时间来说都很重要，存在对连动系统结束处理时间的限制', '0');
INSERT INTO `sys_dictionary` VALUES ('6fd1d74d99dd469d9af57ac127d053e0', '4', 'pro_project', 'development_language', '其他', '1');
INSERT INTO `sys_dictionary` VALUES ('75043f7dcb4e4887a41f9b4ff0568761', '2', 'pro_project', 'performance', '没有明示对性能的特别需求事项或仅需提供基本性能', '1');
INSERT INTO `sys_dictionary` VALUES ('795f62e5fa084284befb9c10e595deae', '3', 'pro_project', 'development_language', 'C及其他同级别语言/平台', '1.5');
INSERT INTO `sys_dictionary` VALUES ('797f12808c054a22a2862b8b7f26f773', '1', 'pro_project', 'team_background', '为其他行业开发过类似的软件，或为本行业开发过不同但相关的软件', '1');
INSERT INTO `sys_dictionary` VALUES ('806d3647645241c295a01f801c33eddb', '1', 'pro_project', 'development_language', 'JAVA、C++、C#及其他同级别语言/平台', '1');
INSERT INTO `sys_dictionary` VALUES ('9bdcb4e6cce14167945f701b6b99db90', '8', 'pro_project', 'application_type', '流程控制', '2.0');
INSERT INTO `sys_dictionary` VALUES ('a5659977b03141da9488d33405b921f7', '3', 'pro_project', 'application_type', '科技', '1.2');
INSERT INTO `sys_dictionary` VALUES ('a9d5897b84a04d5aae888544c1847587', '3', 'pro_project', 'performance', '为满足性能需求事项，要求设计阶段开始进行性能分析，或在设计、开发阶段使用分析工具', '-1');
INSERT INTO `sys_dictionary` VALUES ('bb82412693134ed985180c23128515be', '5', 'pro_project', 'application_type', '智能信息', '1.7');
INSERT INTO `sys_dictionary` VALUES ('bbd77300a3be41d8809622e752f15116', '3', 'pro_project', 'team_background', '没有同类软件及本行业相关软件开发背景', '1.2');
INSERT INTO `sys_dictionary` VALUES ('cbf3a17fbb6048588add834ff2a46660', '2', 'pro_project', 'opportunity', '项目中期(投标、商务谈判)', '1.26');
INSERT INTO `sys_dictionary` VALUES ('d22ae0db74444bea893189fa5ca1ac0b', '1', 'pro_project', 'opportunity', '项目早期(立项、预算)', '1.50');
INSERT INTO `sys_dictionary` VALUES ('d543f0cd464f4bf39c2bc58f754a7486', '4', 'pro_project', 'application_type', '多媒体', '1.3');
INSERT INTO `sys_dictionary` VALUES ('e58af4f165ea46bd96ea747d92f6c51a', '1', 'pro_project', 'reliability', '发生故障时带来较多不便或经济损失', '0');
INSERT INTO `sys_dictionary` VALUES ('eb9467f41b234f938cf8579b6a7753cd', '1', 'pro_project', 'demand_grade', 'A', '1.50');
INSERT INTO `sys_dictionary` VALUES ('ebcfde32ec02440abf60ca6f314057a5', '1', 'pro_project', 'multiple_sites', '在设计阶段需要考虑不同站点的相似硬件或软件环境下运行需求', '0');
INSERT INTO `sys_dictionary` VALUES ('fcab582f13854a46a31a38bd51bd03e7', '3', 'pro_project', 'reliability', '发生故障时造成重大经济损失或有生命危害', '-1');

-- ----------------------------
-- Table structure for sys_login_log
-- ----------------------------
DROP TABLE IF EXISTS `sys_login_log`;
CREATE TABLE `sys_login_log` (
  `id` varchar(32) NOT NULL COMMENT '主键ID',
  `token` varchar(100) DEFAULT NULL COMMENT 'token',
  `ip` varchar(100) DEFAULT NULL COMMENT '访问地址',
  `create_time` datetime DEFAULT NULL,
  `username` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户名',
  `status` int(2) DEFAULT NULL COMMENT '0失败1成功',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='SYS登录系统日志表';

-- ----------------------------
-- Records of sys_login_log
-- ----------------------------
INSERT INTO `sys_login_log` VALUES ('00aa247ab711437fa75761e2748c1e40', '7016655d6d945fd94d0d311237cebf7a', '127.0.0.1', '2019-04-16 16:11:21', 'test', '1');
INSERT INTO `sys_login_log` VALUES ('06e72191afe04b14aee7172d135ef963', '7016655d6d945fd94d0d311237cebf7a', '127.0.0.1', '2019-04-16 17:13:16', 'test', '1');
INSERT INTO `sys_login_log` VALUES ('190cbb31f87a4f07916dcce49c0a4c8d', 'b132b1dd8506501a5752a9ea7a44399f', '127.0.0.1', '2019-04-16 16:21:06', 'admin', '1');
INSERT INTO `sys_login_log` VALUES ('2c28ad9de05741a58dffb34731f0314e', null, '127.0.0.1', '2019-04-16 16:20:59', 'admin1111', '0');
INSERT INTO `sys_login_log` VALUES ('496e21afd17d44c49f96af810063b91c', 'b132b1dd8506501a5752a9ea7a44399f', '127.0.0.1', '2019-04-17 10:21:27', 'admin', '1');
INSERT INTO `sys_login_log` VALUES ('4c0b861450c844d08a54faae21f520d3', 'b132b1dd8506501a5752a9ea7a44399f', '127.0.0.1', '2019-04-16 16:11:37', 'admin', '1');
INSERT INTO `sys_login_log` VALUES ('72aa2b8b8c5742bb9d522b9b5719bca4', null, '127.0.0.1', '2019-04-16 16:20:57', 'admin1111', '0');
INSERT INTO `sys_login_log` VALUES ('8973a24f7059438abc5f4d287d0b40eb', 'b132b1dd8506501a5752a9ea7a44399f', '127.0.0.1', '2019-04-17 08:49:18', 'admin', '1');
INSERT INTO `sys_login_log` VALUES ('90ff44d70d334af6908b8a8195d56f6f', 'b132b1dd8506501a5752a9ea7a44399f', '127.0.0.1', '2019-04-17 09:41:23', 'admin', '1');
INSERT INTO `sys_login_log` VALUES ('a2b78697cf7548189caf4c3e64d26551', 'b132b1dd8506501a5752a9ea7a44399f', '127.0.0.1', '2019-04-17 09:36:11', 'admin', '1');
INSERT INTO `sys_login_log` VALUES ('beaad3955875486292d7669df9fb317b', 'b132b1dd8506501a5752a9ea7a44399f', '127.0.0.1', '2019-04-22 14:14:58', 'admin', '1');
INSERT INTO `sys_login_log` VALUES ('c83a4ba19fab4343a7b20f52d1c91b25', 'b132b1dd8506501a5752a9ea7a44399f', '127.0.0.1', '2019-04-17 08:49:21', 'admin', '1');
INSERT INTO `sys_login_log` VALUES ('f1d6fac774ab48c59f24bf425b2d7340', 'b132b1dd8506501a5752a9ea7a44399f', '127.0.0.1', '2019-04-16 16:10:53', 'admin', '1');

-- ----------------------------
-- Table structure for sys_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu` (
  `id` varchar(32) NOT NULL COMMENT '主键ID',
  `menu_name` varchar(50) NOT NULL COMMENT '角色名称',
  `url` varchar(100) NOT NULL,
  `icon` varchar(50) DEFAULT NULL COMMENT '图标',
  `order` int(1) DEFAULT NULL COMMENT '排序',
  `type` int(1) DEFAULT '1' COMMENT '类型:1菜单,2按钮',
  `status` int(1) DEFAULT '1' COMMENT '状态0注销1正常',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `pid` varchar(32) DEFAULT '' COMMENT '父ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='SYS菜单表';

-- ----------------------------
-- Records of sys_menu
-- ----------------------------
INSERT INTO `sys_menu` VALUES ('06b90c1dd21b479ab8e7b3ff33b6c25a', '爬虫管理', '/', 'el-icon-lx-friend', '98', '1', '1', '2019-04-16 14:03:42', '2019-04-16 14:03:42', '');
INSERT INTO `sys_menu` VALUES ('287979ad70764a28816485528cd528ca', '系统首页', 'dashboard', 'el-icon-lx-home', '1', '44', '1', '2019-04-11 20:27:42', '2019-04-11 20:27:42', '');
INSERT INTO `sys_menu` VALUES ('3cf3d22a388943e89f5176641fb9ec02', '用户管理', 'userTable', '', '2', '1', '1', '2019-04-16 14:03:44', '2019-04-16 14:03:44', 'be72dfa9914a4748b07ff50af301c14a');
INSERT INTO `sys_menu` VALUES ('4e402889c313465d90eea2230277e3ab', '日志管理', 'logTable', '', '4', '1', '1', '2019-04-16 15:19:56', '2019-04-16 15:19:56', 'be72dfa9914a4748b07ff50af301c14a');
INSERT INTO `sys_menu` VALUES ('74b5328ed49e4ad8b14cb1167f54342a', '角色管理', 'roleTable', '', '3', '1', '1', '2019-04-16 14:03:41', '2019-04-16 14:03:41', 'be72dfa9914a4748b07ff50af301c14a');
INSERT INTO `sys_menu` VALUES ('8493542e1ddf4d819835b2853ce446c9', '菜单管理', 'menuTable', '', '4', '1', '1', '2019-04-16 14:03:34', '2019-04-16 14:03:34', 'be72dfa9914a4748b07ff50af301c14a');
INSERT INTO `sys_menu` VALUES ('be72dfa9914a4748b07ff50af301c14a', '系统管理', '/', 'el-icon-lx-settings', '99', '1', '1', '2019-04-16 14:03:32', '2019-04-16 14:03:32', '');

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role` (
  `id` varchar(32) NOT NULL COMMENT '主键ID',
  `role_name` varchar(50) DEFAULT NULL COMMENT '角色名称',
  `describe` varchar(100) DEFAULT NULL COMMENT '角色描述',
  `status` int(1) DEFAULT '1' COMMENT '状态0注销1正常',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='SYS角色表';

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role` VALUES ('6e798b477125486b9c3f1b50ff6ded6c', '管理员', '管理员角色', '1', '2019-04-16 17:13:00', '2019-04-16 17:12:59');
INSERT INTO `sys_role` VALUES ('da4f11b2232e488abcef783171f04761', '超级管理员', '拥有所有权限菜单', '1', '2019-04-16 15:23:32', '2019-04-16 15:23:32');

-- ----------------------------
-- Table structure for sys_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_menu`;
CREATE TABLE `sys_role_menu` (
  `id` varchar(32) NOT NULL COMMENT '主键ID',
  `role_id` varchar(32) DEFAULT NULL COMMENT '角色ID',
  `menu_id` varchar(32) DEFAULT NULL COMMENT '菜单ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='SYS角色菜单关联表';

-- ----------------------------
-- Records of sys_role_menu
-- ----------------------------
INSERT INTO `sys_role_menu` VALUES ('069f7ea077b84395ae8fc234eca81d72', 'da4f11b2232e488abcef783171f04761', '4e402889c313465d90eea2230277e3ab');
INSERT INTO `sys_role_menu` VALUES ('0f490e2fa7914ee1820226dd71377814', 'da4f11b2232e488abcef783171f04761', '287979ad70764a28816485528cd528ca');
INSERT INTO `sys_role_menu` VALUES ('52e551812b0a4a3692200d81a7802ad9', '6e798b477125486b9c3f1b50ff6ded6c', '4e402889c313465d90eea2230277e3ab');
INSERT INTO `sys_role_menu` VALUES ('5ae3f1d31a9e4953b33b315e832429a0', 'da4f11b2232e488abcef783171f04761', '06b90c1dd21b479ab8e7b3ff33b6c25a');
INSERT INTO `sys_role_menu` VALUES ('5eb482339c60403d976383afdda0a2f7', '6e798b477125486b9c3f1b50ff6ded6c', 'be72dfa9914a4748b07ff50af301c14a');
INSERT INTO `sys_role_menu` VALUES ('90200f81e6ec40daa556db16dc97e955', 'da4f11b2232e488abcef783171f04761', '3cf3d22a388943e89f5176641fb9ec02');
INSERT INTO `sys_role_menu` VALUES ('90e6a37892994a238aee7e47fb9b74a0', '6e798b477125486b9c3f1b50ff6ded6c', '3cf3d22a388943e89f5176641fb9ec02');
INSERT INTO `sys_role_menu` VALUES ('a6f2c6a49cbb4318bf9483f96fdcaaed', 'da4f11b2232e488abcef783171f04761', 'be72dfa9914a4748b07ff50af301c14a');
INSERT INTO `sys_role_menu` VALUES ('b1119bd462fd43558c3d8327815000fc', 'da4f11b2232e488abcef783171f04761', '74b5328ed49e4ad8b14cb1167f54342a');
INSERT INTO `sys_role_menu` VALUES ('cd7ff1cd34d041f79597e98ab3647c45', 'da4f11b2232e488abcef783171f04761', '8493542e1ddf4d819835b2853ce446c9');
INSERT INTO `sys_role_menu` VALUES ('fb2ec37dc37b4595a16e7ed9228f90ff', '6e798b477125486b9c3f1b50ff6ded6c', '287979ad70764a28816485528cd528ca');

-- ----------------------------
-- Table structure for sys_system_log
-- ----------------------------
DROP TABLE IF EXISTS `sys_system_log`;
CREATE TABLE `sys_system_log` (
  `id` varchar(32) NOT NULL COMMENT '主键ID',
  `requestURL` varchar(32) DEFAULT NULL COMMENT '请求路径',
  `requestIP` varchar(20) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `describe` varchar(100) DEFAULT NULL COMMENT '描述',
  `returnCODE` int(4) DEFAULT NULL,
  `msg` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='SYS系统日志表';

-- ----------------------------
-- Records of sys_system_log
-- ----------------------------

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user` (
  `id` varchar(32) NOT NULL COMMENT '主键ID',
  `username` varchar(50) DEFAULT NULL COMMENT '用户名(登录名)',
  `password` varchar(50) DEFAULT NULL COMMENT '密码',
  `status` int(1) DEFAULT '1' COMMENT '状态0注销1正常',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `mobile` varchar(100) DEFAULT NULL COMMENT '手机号',
  `create_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='SYS角色表';

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES ('d355e0fa49e042e680167caf8eb191cb', 'admin', '670b14728ad9902aecba32e22fa4f6bd', '1', '123@qq.com', '123123', '2019-04-16 13:30:45', '2019-04-16 13:30:45');
INSERT INTO `sys_user` VALUES ('fef6fa60a14643639cf4c6c08ce9628d', 'test', '670b14728ad9902aecba32e22fa4f6bd', '1', '123@qq.com', '123123123', '2019-04-16 17:13:10', '2019-04-16 17:13:10');

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role` (
  `id` varchar(32) NOT NULL COMMENT '主键ID',
  `user_id` varchar(32) DEFAULT NULL COMMENT '用户ID',
  `role_id` varchar(32) DEFAULT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='SYS用户角色关联表';

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------
INSERT INTO `sys_user_role` VALUES ('1c95422d57e246efb8ea80daa6dedb39', 'fef6fa60a14643639cf4c6c08ce9628d', '6e798b477125486b9c3f1b50ff6ded6c');
INSERT INTO `sys_user_role` VALUES ('479e23994bdc4acd8506bebb06bb765a', 'd355e0fa49e042e680167caf8eb191cb', 'da4f11b2232e488abcef783171f04761');
