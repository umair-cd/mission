import * as $ from "jquery";
import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import {on, Options} from "../utils/decorators";


@Options({
    template: false,
    el: "body",
    ui: {
        contactIframe: "#contact-iframe",
        headerHero: ".header-hero",
        contactIframeTest: ".contact-iframe-test"
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
       
    }

    onRender() {
        console.log("Contact US Rendered!");
    }
}
