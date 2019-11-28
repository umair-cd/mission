import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import {on, Options} from "../utils/decorators";


@Options({
    template: false,
    el: "body",
    ui: {
        dropDown:".select-selected",
        dropDownOptions: "#options",
        questions:".questions",
        loadMoreButtons:".load-more", 
        goToLinksDesktop: ".questions-menu",
        goTolinksMobile: ".custom-select #options"
    }
})
export default class ViewController extends Marionette.View<Backbone.Model>{
    constructor() {
        super();
        this.goToSectionMobile();
        this.goToSectionDesktop();
    }

    initialize() {
        this.addEventListeners();
    }

    goToSectionDesktop() {
        this.ui.goToLinksDesktop.on("click", 'a[href^="#"]', function(event) {
            event.preventDefault();
            console.log("this was clicked");
            $("html, body").animate(
                {
                    scrollTop: $($(this).attr("href")).offset().top - 120
                },
                1000
            );
        console.log("clicked this");
        });
    }

    goToSectionMobile() {
        this.ui.goTolinksMobile.on("click", 'a[href^="#"]', function(event) {
            event.preventDefault();
            console.log("this was clicked");
            $("html, body").animate(
                {
                    scrollTop: $($(this).attr("href")).offset().top - 70
                },
                1000
            );
        console.log("clicked this");
        });
    }

    addEventListeners() {
        this.ui.dropDown.on('click',this.onDropDownClick.bind(this));
        this.ui.dropDownOptions.children().on('click',this.onDropDownOptionClick.bind(this))
        this.ui.questions.children(".questions-item").on('click',this.onQuestionClick.bind(this));
        this.ui.loadMoreButtons.on('click',this.onLoadMoreClick.bind(this));
        //$( document ).on('click',()=>{this.ui.dropDownOptions.toggleClass("select-hide");});
    }

    onDropDownClick(){
        this.ui.dropDownOptions.toggleClass("select-hide");
    }

    onDropDownOptionClick(e){
        this.ui.dropDown.html($(e.currentTarget).text());
        this.ui.dropDownOptions.toggleClass("select-hide");
        this.ui.dropDownOptions.children(".same-as-selected").removeClass("same-as-selected")
        $(e.currentTarget).addClass("same-as-selected");
    }
    onQuestionClick(e){
        $(e.currentTarget).toggleClass("show-answer");
    }
    onLoadMoreClick(e){
        $(e.currentTarget).siblings("div:hidden").slice(0, 10).show();
        if($(e.currentTarget).siblings("div:hidden").length == 0){
            $(e.currentTarget).hide(); 
        }
    }
    onRender() {
        console.log("FAQ ViewController Rendered!");
    }
}
