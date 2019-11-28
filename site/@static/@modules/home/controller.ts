import * as Backbone from 'backbone';
import * as Marionette from 'backbone.marionette';
import * as _ from 'underscore';
import { on, Options } from '../utils/decorators';

@Options({
    template: false,
    el: 'body',
    ui: {
        carousel: '.js-home-carousel',
        slides: '.js-carousel-slide',
        featuredRecipes: '.js-featured-recipes',
        featuredProducts: '.js-featured-products-carousel',
        relatedRecipes: '.js-related-recipes-carousel',
        recipeCards: '.js-related-recipe-items',
        featuredProductTitle: '.featured-product-title',
        featuredProductLink: '.featured-product-link',
        carouselButton: '.slide-cta',
        collectionTitles: '.js-collection-title',
        collapsibleCollections: '.js-collapsible-quick-snack',
        homeNavbar: '.navbar',
        desktopNavbarContent: '.desktop-navbar-content',
        heroWindow: '.window'
    }
})
export default class ViewController extends Marionette.View<Backbone.Model> {
    constructor() {
        super();
        this.init();
    }

    onCarouselClick(evt) {
        window.location.replace($(evt.target).attr('href'));
    }

    init() {
        this.initializeCarousels();

        this.rotateCollectionWords();

        this.setStickyElements();

        this.ui.carouselButton.on('click', this.onCarouselClick.bind(this));
        $(document).on('scroll', this._onDocumentScroll.bind(this));
    }

    _onDocumentScroll() {
        this.setStickyElements();
    }

    setStickyElements() {
        var $window = $(window);
        var top = $window.scrollTop() + this.ui.homeNavbar.height() - 50;
        var bottomOfScreen = top + $window.height();
        var bottomOfHero =
            this.ui.heroWindow.offset().top + this.ui.heroWindow.outerHeight();

        if (bottomOfScreen < bottomOfHero) {
            this.ui.collapsibleCollections.addClass('is-fixed');
        } else {
            this.ui.collapsibleCollections.removeClass('is-fixed');
        }
        if (top > bottomOfHero) {
            this.ui.homeNavbar.removeClass('transparent').addClass('is-fixed');
        } else {
            this.ui.homeNavbar.addClass('transparent').removeClass('is-fixed');
        }
    }

    rotateCollectionWords() {
        var titles = this.ui.collectionTitles;
        var next_label, first;
        var max = titles.length;
        var index = 0;
        var active_label = (first = $(titles[0]));
        var title_obj_list = [];

        $(titles).each(function() {
            var title_obj = $(this);

            // Make sure each label is on one-line
            title_obj.css({ 'white-space': 'nowrap' });

            var label_width = title_obj.width();
            title_obj_list.push({
                width: label_width,
                title_obj: title_obj
            });
        });

        // Find the widest label
        var max_label_title_obj = title_obj_list.reduce(function(x, y) {
            if (x['width'] > y['width']) {
                return x;
            } else if (x['width'] < y['width']) {
                return y;
            } else {
                return x || y;
            }
        });

        //Make label underline the width of the widest label width.
        $('.selected-collection')
            .width(max_label_title_obj.width)
            .css({
                'border-bottom': '1px solid white'
            });

        $('.next-selected-label').width(
            $('.next-selected-label')
                .parent()
                .width()
        );

        (function changeText() {
            if ($('#quick-snack-list').attr('aria-expanded') != 'true') {
                if (index > max) {
                    index = 0;
                    active_label = first;
                    next_label = $(titles[index + 1]);
                } else {
                    next_label = $(titles[index + 1]);
                }

                active_label.animate(
                    {},
                    {
                        duration: 4000,
                        complete: function() {
                            var label = $(this);
                            var next = label.next();

                            // Move back to first element
                            if (next.length == 0) {
                                next = first;
                            }
                            label.hide();

                            next.css({
                                display: 'inline-block',
                                'transform-origin': 'bottom',
                                animation: 'rotateXTopsideDown 0.5s ease',
                                'backface-visibility': 'hidden'
                            });
                            // reset label back below fold
                            label.css({
                                animation: '',
                                'transform-origin': '',
                                'backface-visibility': ''
                            });
                        }
                    }
                );
                active_label = next_label;
                index++;
                setTimeout(changeText, 4000);
            }
        })();
    }

    initializeCarousels() {
        this.initializeHomeCarousel();
        this.initializeFeaturedRecipesCarousel();
        this.initializeFeaturedProductsCarousel();
        this.initializeRelatedRecipesCarousel();
        this.initializeRecipeCardsCarousel();
    }

    initializeHomeCarousel() {
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

    initializeFeaturedRecipesCarousel() {
        let options = {
            slidesToShow: 1.1,
            mobileFirst: true,
            infinite: false,
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
                        slidesToShow: 3
                    }
                }
            ]
        };

        this.ui.featuredRecipes.slick(options);
    }

    initializeFeaturedProductsCarousel() {
        let slides = this.ui.featuredProducts.find('.featured-product');
        let initial;

        _.each(slides, function(slide, index) {
            if ($(slide).data('initial') == true) {
                initial = index;
            }
        });

        let options = {
            centerMode: true,
            centerPadding: '100px',
            slidesToShow: 5,
            appendArrows: '.js-arrow-container',
            asNavFor: this.ui.relatedRecipes,
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

        this.ui.featuredProducts.slick(options);

        this.changeTitleonSlideChange(slides, 0);

        this.ui.featuredProducts.on('afterChange', (e, s, curr) =>
            this.changeTitleonSlideChange(slides, curr)
        );
    }

    changeTitleonSlideChange(slides, currentSlide) {
        const slide = $(slides[currentSlide]);
        this.ui.featuredProductTitle.text(slide.attr('prod-title'));
        this.ui.featuredProductLink.prop('href', slide.attr('prod-url'));
        this.ui.featuredProductLink.text(slide.attr('prod-cta'));
    }

    initializeRelatedRecipesCarousel() {
        let options = {
            slidesToShow: 1,
            arrows: false,
            fade: true,
            draggable: false,
            touchMove: false,
            swipe: false
        };

        this.ui.relatedRecipes.slick(options);
    }

    initializeRecipeCardsCarousel() {
        let options = {
            slidesToShow: 1.05,
            infinite: false,
            arrows: false,
            mobileFirst: true,
            swipeToSlide: true,
            responsive: [
                {
                    breakpoint: 376,
                    settings: {
                        slidesToShow: 1.1
                    },
                },
                {
                    breakpoint: 760,
                    settings: {
                        slidesToShow: 4
                    }
                },
            ]
        };

        $.each(this.ui.recipeCards, function(index, card) {
            card = $(card);
            card.slick(options);

            card.on('beforeChange', function(ev) {
                ev.stopPropagation();
            });
        });
    }

    onRender() {
        // Temp
        console.log('Home ViewController Rendered!');
    }
}
