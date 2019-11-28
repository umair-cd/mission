import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import {on, Options} from "../utils/decorators";


@Options({
    template: false,
    el: "body",
    ui: {
        playButton: ".js-video-play-btn",
        iframeWrapper: ".js-iframe-wrapper",
        videoImage: ".js-video-image",
        ytPlayer: "#yt-player"
    }
})
export default class ViewController extends Marionette.View<Backbone.Model>{

    constructor() {
        super();
    }

    initialize() {
        this.addEventListeners();
    }

    addEventListeners() {
        this.ui.playButton.on("click", this.onVideoPlayButtonClick.bind(this));
    }

    onVideoPlayButtonClick(ev) {
        this.ui.videoImage.addClass("inactive");
        this.ui.iframeWrapper.addClass("is-active");
        window["player"].playVideo();
    }

    onRender() {
        // Temp
        console.log("styled video ViewController Rendered!");

    }
}
