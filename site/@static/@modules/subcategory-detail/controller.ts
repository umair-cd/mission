import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import {on, Options} from "../utils/decorators";


@Options({
    template: false,
    el: "body",
    ui: {
        productSubcategoryCarousel: ".js-subcategory-product-carousel"
        
    }
})
export default class ViewController extends Marionette.View<Backbone.Model>{
    constructor() {
        super();
        this.initializeProductSubcategoryCarousel();

    }

    initializeProductSubcategoryCarousel() {
        this.ui.productSubcategoryCarousel.slick({
            dots: false,
            speed: 300,
            slidesToShow: 4,
            slidesToScroll: 4,
            arrows:true, 
            infinite: true, 
            responsive: [ 
                {
                  breakpoint: 1025,
                  settings: {
                      arrows:false,
                      slidesToShow: 3,
                      dots:true
                  }
                },
                {
                  breakpoint: 415,
                  settings: {
                      arrows:false,
                      slidesToShow: 2,
                      dots:true
                  }
                }
            ]
        });
      }

    onRender() {
        // Temp
        console.log("subCategory Detail ViewController Rendered!");
    }

    
}
