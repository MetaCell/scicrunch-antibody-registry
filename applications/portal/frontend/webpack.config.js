const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CompressionPlugin = require("compression-webpack-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

const copyPaths = [
  { from: path.resolve(__dirname, "src/assets"), to: "assets" },
  { from: path.resolve(__dirname, "sitemap.xml"), to: "sitemap.xml" }
];

module.exports = function webpacking(envVariables) {
  let env = envVariables;
  if (!env) {
    env = {};
  }
  if (!env.mode) {
    env.mode = "production";
  }

  console.log("####################");
  console.log("####################");
  console.log("BUILD bundle with parameters:");
  console.log(env);
  console.log("####################");
  console.log("####################");

  const { mode } = env;
  const devtool = "source-map";

  const output = {
    path: path.resolve(__dirname, "dist"),
    filename: "[name].[contenthash].js",
    publicPath: "/"
  };

  const module = {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
      },
      {
        test: /\.ts(x?)$/,
        include: path.resolve(__dirname, 'src'),
        use: [
          {
            loader: "ts-loader",
            options: {
              transpileOnly: true,
            },
          }
        ]
      }
    ],
  };

  const resolve = {
    extensions: ["*", ".js", ".json", ".ts", ".tsx", ".jsx"],
    symlinks: false,
  };

  const plugins = [
    new CleanWebpackPlugin(),
    new CopyWebpackPlugin({ patterns: copyPaths }),
    new CompressionPlugin(),
    new HtmlWebpackPlugin({
      template: "src/index.ejs",
      favicon: path.join(__dirname, "src/assets/logo.svg"),
    }),
  ];

  return {
    mode,
    devtool,
    output,
    module,
    resolve,
    plugins,
  };
};
