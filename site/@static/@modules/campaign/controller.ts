import * as Backbone from 'backbone';
import * as Marionette from 'backbone.marionette';
import { Options } from '../utils/decorators';

@Options({
    template: false,
    el: 'body',
    ui: {
        heroCarousel: '.campaign-carousel',
        heroSlides: '.campaign-carousel-slide',
        additionalProductsCarousel: '.additional-products-carousel',
        influencerCarousel: '.influencer-carousel',
        heroButton: '.hero-button:first',
    },
})
export default class ViewController extends Marionette.View<Backbone.Model> {
    constructor() {
        super();
        this.init();
    }

    init() {
        this.initializeHeroCarousel();
        this.initializeAdditionalProductsCarousel();
        this.initializeInfluencerCarousel();
        this.appendHeroButton();
    }

    initializeHeroCarousel() {
        const options = {
            fade: true,
            adaptiveHeight: true,
            mobileFirst: true,
            rows: 0,
            arrows: false,
            autoplay: true,
            autoplaySpeed: 5000,
        };

        if (this.ui.heroSlides.length > 1) {
            this.ui.heroCarousel.slick(options);
        }
    }

    initializeAdditionalProductsCarousel() {
        const options = {
            centerMode: true,
            centerPadding: '100px',
            slidesToShow: 5,
            initialSlide: 0,
            appendArrows: '.product-arrow-container',
            infinite: true,
            lazyLoad: 'ondemand',
            responsive: [
                {
                    breakpoint: 760,
                    settings: {
                        variableWidth: false,
                        slidesToShow: 1,
                        centerPadding: '25%',
                        arrows: false
                    }
                }
            ]
        };

        this.ui.additionalProductsCarousel.slick(options);
    }

    initializeInfluencerCarousel() {
        const options = {
            slidesToShow: 3,
            initialSlide: 0,
            appendArrows: '.influencer-arrow-container',
            infinite: false,
            responsive: [
                {
                    breakpoint: 1368,
                    settings: {
                        slidesToShow: 2,
                        arrows: false,
                    }
                },
                {
                    breakpoint: 760,
                    settings: {
                        adaptiveHeight: true,
                        slidesToShow: 1,
                        centerMode: true,
                        centerPadding: 50,
                        arrows: false
                    }
                }
            ]
        };

        this.ui.influencerCarousel.slick(options);
    }

    appendHeroButton() {
        this.ui.heroButton.clone().appendTo('#product-button');
    }

    onRender() {
        console.log('Campaign ViewController Rendered!');
    }
}
