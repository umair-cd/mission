import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import { on, Options } from "../utils/decorators";

@Options({
    template: false,
    el: "body",
    ui: {}
})
export default class ViewController extends Marionette.View<Backbone.Model> {
    constructor() {
        super();
        this.addEventListeners();
    }

    addEvent(el, evt, fn) {
        if (el.addEventListener) {
            el.addEventListener(evt, fn);
        } else if (el.attachEvent) {
            el.attachEvent("on" + evt, function(evt) {
                fn.call(el, evt);
            });
        } else if (
            typeof el["on" + evt] === "undefined" ||
            el["on" + evt] === null
        ) {
            el["on" + evt] = function(evt) {
                fn.call(el, evt);
            };
        }
    }

    addMessageEvent() {
        this.addEvent(window, "message", function(message) {
            var dataLayer = window["dataLayer"] || (window["dataLayer"] = []);
            var data = message.data.split(":");
            if (
                data[0] === "SRCH" &&
                message.origin === "http://destinilocators.com"
            ) {
                dataLayer.push({
                    event: "locationSearched",
                    locationSearched: data[1]
                });
            } else if (
                message.data === "RSIZ:820" &&
                message.origin === "http://destinilocators.com"
            ) {
                dataLayer.push({
                    event: "buyOnlineClick"
                })
            }
        });
    }

    addEventListeners() {
        this.addMessageEvent();
    }

    onRender() {
        // Temp
        console.log("Where-To-Buy ViewController Rendered!");
    }
}
