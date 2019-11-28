import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import { on, Options } from "../utils/decorators";

@Options({
    template: false,
    el: "body",
    ui: {
        productSubcategoryCarousel: ".js-subcategory-product-carousel",
        carouselCard: ".product-item",
        mobileCategories: ".js-mobile-select-menu",
        background: ".js-background",
        subcategory: ".js-subcategory-navigation"
    }
})
export default class ViewController extends Marionette.View<Backbone.Model> {
    constructor() {
        super();
        this.initializeProductSubcategoryCarousel();
        this.linkToSection();
    }

    initialize() {
        $(document).on("scroll", this._onDocumentScroll.bind(this));
    }

    linkToSection() {
        this.ui.subcategory.on("click", 'a[href^="#"]', function(event) {
            event.preventDefault();
            console.log("this was clicked");
            $("html, body").animate(
                {
                    scrollTop: $($(this).attr("href")).offset().top - 30
                },
                1000
            );
        });
    }

    initializeProductSubcategoryCarousel() {
        this.ui.productSubcategoryCarousel.slick({
            dots: false,
            speed: 700,
            slidesToShow: 4,
            slidesToScroll: 4,
            arrows: true,
            infinite: true,
            responsive: [
                {
                    breakpoint: 1025,
                    settings: {
                        arrows: false,
                        slidesToShow: 3,
                        slidesToScroll: 3,
                        dots: true
                    }
                },
                {
                    breakpoint: 415,
                    settings: {
                        arrows: false,
                        slidesToShow: 2,
                        slidesToScroll: 2,
                        dots: true
                    }
                }
            ]
        });
    }

    setStickyElements() {
        var top = $(window).scrollTop();
        var trigger = this.ui.background.offset().top;
        var elem = this.ui.mobileCategories;

        if (top > trigger) {
            elem.addClass("sticky");
        } else {
            elem.removeClass("sticky");
        }
    }

    _onDocumentScroll() {
        this.setStickyElements();
    }

    onRender() {
        // Temp
        console.log("Category Detail ViewController Rendered!");
    }
}
