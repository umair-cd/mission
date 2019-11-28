import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import {on, Options} from "../utils/decorators";


@Options({
    template: false,
    el: "body",
    ui: {
        thumbs: ".js-product-thumbnail-container",
        mainImage: ".js-product-detail-main-image",
        thumbCarousel: ".js-product-thumbnails",
        relatedRecipes: ".product-related-recipes .related-recipes",
        relatedProducts: ".related-products .js-related-products",
        buyNow: ".js-buy-now"
    }
})
export default class ViewController extends Marionette.View<Backbone.Model>{

    _MAIN_IMAGE_SRC_
    _THUMB_EVENTS_PRESENT_ = true

    constructor() {
        super();
    }

    initialize() {
        this.initializeProductDetailMainImage();
        this.initializeThumbnailCarousel();
        this.initializeRelatedRecipesCarousel();
        this.addEventListeners();
        this.initializeRelatedProductsCarousel();
    }

    addEventListeners() {
        this.addThumbEventListeners();
        this.addDestiniWidgetListener();

        $(window).on("resize", () => {
            if ($(window).width() <= 768 && !this.ui.thumbCarousel.hasClass("slick-initialized")) {
                this.initializeThumbnailCarousel();
                this._THUMB_EVENTS_PRESENT_ = false;
            }

            if ($(window).width() > 768 && !this._THUMB_EVENTS_PRESENT_) {
                this._THUMB_EVENTS_PRESENT_ = true;
                _.delay(this.addThumbEventListeners.bind(this), 200);
            }
        });
    }

    addThumbEventListeners() {
        this.ui.thumbs.on("mouseenter", this.onThumbMouseEnter.bind(this));
        this.ui.thumbs.on("mouseleave", this.onThumbMouseLeave.bind(this));
        this.ui.thumbs.on("click", this.setActiveMainImage.bind(this));
    }

    addDestiniWidgetListener() {
        this.ui.buyNow.on("click", this.onWhereToBuyClick);
    }

    initializeProductDetailMainImage() {

        _.each(this.ui.thumbs, function(thumb) {
            let thumbnail = $(thumb);
            if (thumbnail.hasClass("is-active")) {
                this.ui.mainImage.attr("src", thumbnail.find(".product-thumbnail").attr("src"));
                this._MAIN_IMAGE_SRC_ = thumbnail.find(".product-thumbnail").attr("src");
            }
        }.bind(this));
    }

    initializeThumbnailCarousel() {
        let options = {
            slidesToShow: 1,
            dots: true,
            infinite: true,
            mobileFirst: true,
            responsive: [
                {
                    breakpoint: 760,
                    settings: "unslick"
                }
            ]
        }

        this.ui.thumbCarousel.slick(options);
    }

    initializeRelatedRecipesCarousel() {
        let options = {
            slidesToShow: 1.05,
            infinite: false,
            arrows: false,
            mobileFirst: true,
            swipeToSlide: true,
            responsive: [
                {
                    breakpoint: 400,
                    settings: {
                        slidesToShow: 1.1
                    }
                },
                {
                    breakpoint: 767,
                    settings: "unslick"
                }
            ]
        };

        this.ui.relatedRecipes.slick(options);
    }

    initializeRelatedProductsCarousel() {
        let options = {
            slidesToShow: 2,
            slidesToScroll: 2,
            infinite: false,
            mobileFirst: true,
            dots: true,
            responsive: [
                {
                    breakpoint: 320,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 2,
                        arrows: false
                    }
                },
                {
                    breakpoint: 768,
                    settings: "unslick"
                }
            ]
        };

        this.ui.relatedProducts.slick(options);
    }

    onThumbMouseEnter(ev) {
        let thumbSrc = $(ev.currentTarget).find(".product-thumbnail").attr("src");
        this.ui.mainImage.attr("src", thumbSrc);
    }

    onThumbMouseLeave(ev) {
        this.ui.mainImage.attr("src", this._MAIN_IMAGE_SRC_);
    }

    onWhereToBuyClick(ev) {
        var $this = $(this);
        var container = $this.attr("data-destini-container");
        var association = $this.attr("data-destini-association");
        window["destini"].init(container);
        window["destini"].loadWidget(association);
    }

    setActiveMainImage(ev) {
        let target = $(ev.currentTarget);
        let targetSrc = target.find(".product-thumbnail").attr("src");

        _.each(this.ui.thumbs, function(thumb) {
            let thumbnail = $(thumb);
            thumbnail.removeClass("is-active");
        }.bind(this));

        target.addClass("is-active");
        this.ui.mainImage.attr("src", targetSrc);
        this._MAIN_IMAGE_SRC_ = targetSrc;
    }

    onRender() {
        // Temp
        console.log("Product Detail ViewController Rendered!");

    }
}
