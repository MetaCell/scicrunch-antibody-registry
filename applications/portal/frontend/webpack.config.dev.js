const { merge } = require('webpack-merge');
const common = require('./webpack.config.js');

var path = require('path');

const PORT = 9000;


module.exports = env => {

  const theDomain = env && env.DOMAIN ? env.DOMAIN : 'localhost:5000';
  
  console.log('Dev server address: ', theDomain);

  const proxyTarget = theDomain;
  const replaceHost = (uri, appName) => (uri.includes("areg-portal") && uri.replace("areg-portal", appName + '.' + theDomain)) || uri;
  if (!env.port) {
    env.devPort = PORT;
  }


  const devServer = {
    static: [{
      directory: path.resolve(__dirname, 'dist'),
      publicPath: '/',
    }],
    compress: true,
    port: Number(env.devPort),
    allowedHosts: "all",
    historyApiFallback: true,
    proxy: {
      '/api/': {
        target: replaceHost( proxyTarget, 'areg-portal'),
        secure: false,
        changeOrigin: true,
      }
    },
  };

  return merge(
    common(env),
    {
      mode: 'development',
      devtool: 'source-map',
      devServer,
    } 
  )
};
