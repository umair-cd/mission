import * as $ from "jquery";
import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import {on, Options} from "../utils/decorators";


@Options({
    template: false,
    el: "body",
    ui: { 
        timelineCarousel: ".js-timeline-carousel", 
        timelineCurrentSlide: ".js-timeline-carousel .slick-current",
        missionUs: "#js-mission-us-title",
        aroundGlobe: "#js-global-title", 
        globeSlide: ".around-globe",
        missionUsSlide: ".mission-us",
        timelineSlide: ".timeline-slide",
        mapCarousel: ".js-map-carousel",
        mapNav: ".js-map-nav",
        map1: ".map-1",
        current: ".slick-current",
        slide: ".slick-slide"

    }
})
export default class ViewController extends Marionette.View<Backbone.Model>{
    constructor() {
        super();
    }

    initialize() {
        this.addEventListeners();
        this.initializeTimelineCarousel();  
        this.initializeMapCarousel();
        this.initializeMapNav();
        this.removeActiveClass();
    }

    addEventListeners() {
       this.ui.missionUs.on("click", this.goToMissionUs.bind(this));
       this.ui.aroundGlobe.on("click", this.goToAroundGlobe.bind(this));
       this.ui.timelineCarousel.on("afterChange", this.changeSlide.bind(this));
    }

    //remove active class for map nav on load 
    removeActiveClass() {
        this.ui.map1.parent().parent().removeClass("slick-current");
    }

    initializeTimelineCarousel() {
        let options = {
            slidesToShow: 1,
            infinite: false,
            arrows: false,
            mobileFirst: true,
            swipeToSlide: true,
            responsive: [
                {
                    breakpoint: 767,
                    settings: {
                         arrows: true    
                    }
                }
            ]
        }

        this.ui.timelineCarousel.slick(options);
    }

    changeSlide(event, slick, currentSlide, nextSlide) {
        var currentSlide = this.ui.timelineCarousel.slick('slickCurrentSlide');
        var missionSlides = this.ui.missionUsSlide.length; 
        var globeSlides = this.ui.globeSlide.length;
        var totalSlides = missionSlides + globeSlides; 

        //console.log("current slides", currentSlide + 1);
        //console.log("mission slides", missionSlides);
        //console.log("globe slides", globeSlides);

        if ((currentSlide >= 0 && currentSlide < missionSlides)) { 
            this.ui.aroundGlobe.removeClass("active"); 
            this.ui.missionUs.addClass("active"); 
        }

        if ((currentSlide >= missionSlides && currentSlide < totalSlides)) { 
            console.log("global slide is active");
            this.ui.missionUs.removeClass("active"); 
            this.ui.aroundGlobe.addClass("active"); 
        }

    }

    goToMissionUs() {
        console.log("mission us"); 
        //always go the the begging of mission us slider 
        this.ui.timelineCarousel.slick("slickGoTo", 0);

        //toggle active class
        this.ui.missionUs.toggleClass("active");
        this.ui.aroundGlobe.toggleClass("active");
    }

    goToAroundGlobe() {
        console.log("global title");

        // find number of mission slides 
        let missionSlidesNumb = this.ui.missionUsSlide.length; 
        // go to mission us slide + 1  
        this.ui.timelineCarousel.slick("slickGoTo", missionSlidesNumb);

        //toggle active class
        this.ui.missionUs.toggleClass("active");
        this.ui.aroundGlobe.toggleClass("active");

    }

    initializeMapCarousel() {
        let options = {
            initialSlide: 6, 
            slidesToShow: 1,
            infinite: false,
            arrows: false,
            dots: true, 
            mobileFirst: true,
            swipe: false,
            fade: true,
            asNavFor: '.js-map-nav',
            speed: 10
            
        }

        this.ui.mapCarousel.slick(options);
    }

    initializeMapNav() {
        let options = { 
            slidesToShow: 6,
            centerMode: true, 
            infinite: false,
            arrows: false,
            dots: false, 
            swipe: false,
            asNavFor: '.js-map-carousel', 
            focusOnSelect: true,
            speed: 10
        }

        this.ui.mapNav.slick(options);
    }

    onRender() {
        console.log("Our History Rendered!");
    }
}
