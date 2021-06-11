const paths = require('./paths')
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  entry: [paths.src + '/index.js'],
  output: {
    filename: 'bundle.js',
    path: paths.build,
  },
  //devtool: 'inline-source-map',
  module : {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ["babel-loader"]
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'webpack Boilerplate',
      template: paths.src + '/template.html', // template file
      filename: 'index.html', // output file
    }),
    //new webpack.HotModuleReplacementPlugin(),
    new webpack.optimize.LimitChunkCountPlugin({
     maxChunks: 1
    }),
    new CleanWebpackPlugin()
  ]
};
