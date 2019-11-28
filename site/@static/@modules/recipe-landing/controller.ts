import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import {on, Options} from "../utils/decorators";


@Options({
    template: false,
    el: "body",
    ui: {
        carousel: ".js-interior-carousel",
        slides: ".js-carousel-slide",
        searchInput: ".js-recipe-search-input",
        resultsHeader: "#results-header"
    }
})
export default class ViewController extends Marionette.View<Backbone.Model>{
    constructor() {
        super();
        this.init();
    }

    init() {
        this.initializeInteriorCarousel();
        this.ui.searchInput.on('focus',this.activateSearch.bind(this));
        this.ui.searchInput.on('blur',this.deactivateSearch.bind(this));
    }

    activateSearch(){
        this.ui.searchInput.prev().addClass("highlight");
    }

    deactivateSearch(){
        this.ui.searchInput.prev().removeClass("highlight");
    }

    initializeInteriorCarousel() {
        let options = {
            fade: true,
            mobileFirst: true,
            rows: 0,
            autoplay: true,
            autoplaySpeed: 5000,
            responsive: [
                {
                    breakpoint: 320,
                    settings: {
                        arrows: false
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        arrows: true
                    }
                }
            ]
        };

        if (this.ui.slides.length > 1) {
            this.ui.carousel.slick(options);
        }
    }

    scrollToResults() {
        if(this.ui.resultsHeader.length > 0) {
            $(window).scrollTop(this.ui.resultsHeader.offset().top - 80);
        }
    }

    onRender() {
        this.scrollToResults();
        // Temp
        console.log("RecipeLanding ViewController Rendered!");

    }
}
