module.exports = {
    pluginOptions: {
        "style-resources-loader": {
            preProcessor: "scss",
            patterns: [path.resolve(__dirname, 'src/styles/global.scss'),]
        }
    }
};
