var webpack = require("webpack");
var path = require("path");
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var BundleTracker = require("webpack-bundle-tracker");
var CopyWebpackPlugin = require("copy-webpack-plugin");
var OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
var publicPath = "/static/";

/**
 * Webpack Docs:
 * - https://webpack.js.org/configuration/
 * - https://webpack.js.org/guides/migrating/ (1.x -> 2.x)
 */

var config = {
    context: path.resolve(__dirname),
    entry: {
        // necessary to copy image files to /static, see README.md
        imgs: "./@imgs/index.js",
        "js/common": "common/index.js",
        "css/common": "common/index.scss",
        "js/ui-kit": "ui-kit/index.js",
        "css/ui-kit": "ui-kit/index.scss",
        "js/home": "home/index.js",
        "css/home": "home/index.scss",
        "js/product-landing": "product-landing/index.js",
        "css/product-landing": "product-landing/index.scss",
        "js/category-detail": "category-detail/index.js",
        "css/category-detail": "category-detail/index.scss",
        "js/subcategory-detail": "subcategory-detail/index.js",
        "css/subcategory-detail": "subcategory-detail/index.scss",
        "js/product-detail": "product-detail/index.js",
        "css/product-detail": "product-detail/index.scss",
        "js/recipe-landing": "recipe-landing/index.js",
        "css/recipe-landing": "recipe-landing/index.scss",
        "css/recipe-detail": "recipe-detail/index.scss",
        "js/recipe-detail": "recipe-detail/index.js",
        "css/collection-landing": "collection-landing/index.scss",
        "css/collection-grid": "collection-grid/index.scss",
        "css/errorPages": "errorPages/index.scss",
        "css/about-us": "about-us/index.scss",
        "css/products-search": "products-search/index.scss",
        "css/sustainability": "sustainability/index.scss",
        "css/faq": "faq/index.scss",
        "js/faq": "faq/index.js",
        "css/careers": "careers/index.scss",
        "css/our-history": "our-history/index.scss",
        "js/our-history": "our-history/index.js",
        "css/contact-us": "contact-us/index.scss",
        "js/contact-us": "contact-us/index.js",
        "js/styled-video": "styled-video/index.js",
        "css/generic": "generic/index.scss",
        "css/where-to-buy": "where-to-buy/index.scss",
        "js/where-to-buy": "where-to-buy/index.js",
        "js/collection-detail": "collection-detail/index.js",
        "js/campaign": "campaign/index.js",
        "css/ccpa-request-form": "ccpa-request-form/index.scss"
    },
    output: {
        path: path.resolve(__dirname, "../static"),
        filename: "[name].js",
        publicPath: publicPath,
        chunkFilename: "[id].chunck.[ext]"
    },
    plugins: [
        new webpack.optimize.CommonsChunkPlugin({
            name: "js/common",
            filename: "js/common.js"
        }),
        new ExtractTextPlugin({ filename: "[name].css" }),
        new BundleTracker({ filename: "../../webpack-stats.json" }),
        new webpack.ProvidePlugin({
            fetch: "imports?this=>global!exports?global.fetch!whatwg-fetch",
            Promise: "bluebird",
            $: "jquery", // bootstrap.js support
            jQuery: "jquery", // bootstrap.js support
            "window.jQuery": "jquery"
        }),
        // SEE: https://github.com/kevlened/copy-webpack-plugin
        new CopyWebpackPlugin([
            // { "from": "@copy/path/to/file.ext", "to": "path/to/file.ext"},
        ])
    ],
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: "css-loader"
                })
            },
            {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract({
                    use: [
                        {
                            loader: "css-loader"
                        },
                        {
                            loader: "sass-loader",
                            options: {
                                data: "$staticUrl: '" + publicPath + "';"
                            }
                        }
                    ]
                })
            },
            {
                test: /\.tsx?/,
                exclude: /node_modules/,
                use: "ts-loader"
            },
            {
                test: /\.(png|gif|jpe?g|svg)$/i,
                exclude: [path.resolve(__dirname, "node_modules")],
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            name: "imgs/[name].[ext]"
                        }
                    },
                    {
                        loader: "image-webpack-loader",
                        options: {
                            mozjpeg: {
                                quality: 65
                            },
                            optipng: {
                                quality: 65
                            },
                            pngquant: {
                                quality: 65
                            },
                            gifsicle: {
                                interlaced: false
                            }
                        }
                    }
                ]
            },
            {
                test: /\.(woff2?|eot|ttf|svg)(\?\S*)?$/,
                exclude: [path.resolve(__dirname, "@imgs")],
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            name: "fonts/[name].[ext]"
                        }
                    }
                ]
            },
            {
                test: /\.(njk|nunjucks)$/,
                exclude: /node_modules/,
                use: {
                    loader: "nunjucks-loader",
                    options: {
                        config: path.resolve(__dirname, "nunjucks.config.js")
                    }
                }
            }
        ]
    },
    devtool: "source-map",
    resolve: {
        extensions: [".webpack.js", "web.js", ".ts", ".tsx", ".js"],
        alias: {
            webworkify: "webworkify-webpack",
            bootstrap: "bootstrap-sass/assets/javascripts/bootstrap",
            "bootstrap-styles": "bootstrap-sass/assets/stylesheets",
            "breakpoint-styles": "breakpoint-sass/stylesheets",
            "bourbon-styles": "bourbon/app/assets/stylesheets"
        },
        modules: ["node_modules", "@modules", "@css", "@imgs", "@tests"]
    },
    stats: { children: false }
};

if (
    process.env.WEBPACK_ENV == "production" ||
    process.env.WEBPACK_ENV === "staging"
) {
    config.plugins = config.plugins.concat([
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                screw_ie8: true,
                warnings: false,
                unsafe: true,
                pure_getters: true
            },
            comments: false,
            sourceMap: true
        }),
        new OptimizeCssAssetsPlugin({
            cssProcessorOptions: {
                safe: true
            }
        })
    ]);

    config.module.rules = config.module.rules.concat([
        {
            test: /\.(js|ts)$/,
            loader: "webpack-strip?strip[]=console.warn,strip[]=console.log"
        }
    ]);
}

module.exports = config;
