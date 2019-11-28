import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import {on, Options} from "../utils/decorators";


@Options({
    template: false,
    el: "body",
    ui: {
        categorySelector: ".js-category-selector",
        mobileCategories: ".js-mobile-select-menu",
        mobileCategorySelector: ".js-mobile-select-menu select",
        categoryTabPage: ".js-category-tab-page",
        categoryGrid: ".js-product-category-grid",
        categoryTabWrapper: ".category-tab-wrapper",
        featureProduct: ".featured-influences"
    }
})
export default class ViewController extends Marionette.View<Backbone.Model>{

    useMobileMenu = this.ui.mobileCategories.css("display") == "block"

    constructor() {
        super();
    }

    initialize() {
        this.addEventListeners();
        this.setStickyElements();
    }

    addEventListeners() {
        this.ui.categorySelector.on("click", this.onChangeActiveCategory.bind(this));
        this.ui.mobileCategorySelector.on("change", this.onChangeMobileActiveCategory.bind(this));
        $(document).on("scroll", this._onDocumentScroll.bind(this));
    }

    onChangeMobileActiveCategory(ev) {
        this._updateCategorTab(ev.currentTarget.value, 'mobile');
    }

    onChangeActiveCategory(ev) {
        let target = $(ev.currentTarget);
        if(!target.hasClass("active")){
            var slug = target.data("slug");
            this.ui.categorySelector.removeClass("active");
            this._updateCategorTab(slug, 'desktop');
        }
    }

    _updateCategorTab(slug, device){
        const offset = device === 'mobile' ? 400 : 250;
        var active_page = $(".js-category-" + slug);
        active_page.addClass("active");
        window.scrollTo({
            top: active_page.offset().top + offset,
            behavior: 'smooth'
        });

        this.ui.categoryTabPage.fadeOut();
        $("#" + slug).fadeIn();
    }

    _onDocumentScroll(){
        this.setStickyElements();
    }

    setStickyElements(){
        var top = $(window).scrollTop();
        var trigger = this.ui.categoryTabWrapper.offset().top - 110;
        var triggerFeaturedProduct =  this.ui.featureProduct.position().top;

        if(this.useMobileMenu){
            var elem = this.ui.mobileCategories;
        } else {
            var elem = this.ui.categoryGrid;
        }

        // if (bottomOfScreen < bottomOfHero) {
        //     this.ui.categoryGrid.addClass('sticky');
        // }else{
        //     this.ui.categoryGrid.removeClass('sticky');
        // }
        if (top > trigger && top < triggerFeaturedProduct){
            elem.addClass('sticky');
        }else{
            elem.removeClass('sticky');
        }
    }

    onRender() {
        // Temp
        console.log("Product Landing ViewController Rendered!");
    }


}
