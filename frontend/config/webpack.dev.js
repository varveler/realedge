const paths = require('./paths')
const webpack = require('webpack');
const dotenv = require('dotenv');
const path = require('path');
const fs = require('fs'); // to check if the file exists
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

const currentPath = path.join(__dirname);
const basePath = currentPath + '/.env';
const envPath = basePath + '.' + 'dev';
const finalPath = fs.existsSync(envPath) ? envPath : basePath;
const fileEnv = dotenv.config({ path: finalPath }).parsed;
const envKeys = Object.keys(fileEnv).reduce((prev, next) => {
    prev[`process.env.${next}`] = JSON.stringify(fileEnv[next]);
    return prev;
  }, {});

module.exports = {
  mode: 'development',
  entry: [paths.src + '/index.js'],
  devtool: 'inline-source-map',
  module : {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ["babel-loader"]
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {loader: 'css-loader', options: {sourceMap: true, importLoaders: 1, modules: true }}
        ]
      }
    ]
  },
  devServer: {
    historyApiFallback: true,
    contentBase: [paths.src, paths.build],
    open: true,
    inline: true,
    hot: true,
    port: 3000,
  },
  plugins: [
    // new CleanWebpackPlugin(['dist/*']) for < v2 versions of CleanWebpackPlugin
    new HtmlWebpackPlugin({
      title: 'webpack Boilerplate',
      template: paths.src + '/template.html', // template file
      filename: 'index.html', // output file
    }),
    new webpack.HotModuleReplacementPlugin(),
    new CleanWebpackPlugin(),
    new webpack.DefinePlugin(envKeys)
  ]
};
