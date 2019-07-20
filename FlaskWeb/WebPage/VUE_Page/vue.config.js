const express = require('express')
const app = express();
const icon = require('./public/icon.json');
var apiRoutes = express.Router();
app.use('/api', apiRoutes);


module.exports = {
    baseUrl: './',
    productionSourceMap: false,
    runtimeCompiler: true,
    devServer: {
        host: '0.0.0.0',
        port: 8888,//端口号
        disableHostCheck : true,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:5000',
                timeout : 6000,
                changeOrigin: true
            }
        },

    }

}