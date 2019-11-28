import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import {on, Options} from "../utils/decorators";


@Options({
    template: false,
    el: "body",
    ui: {
        reviewsLink: '#reviews-link',
        instructionsTab: "#instructions-tab",
        reviewsTab: ".tab-slider--trigger",
        tabs: ".tab-slider--tabs",
        instructionsContent:"#instructions-content",
        reviewsContent:"#reviews-content",
        dropDown:".select-selected",
        dropDownOptions: "#options",
        writeReviewBtn:".write-a-review-btn",
        reviewsModal: ".reviews-modal",
        closeModalBtn: ".close",
        closeModalDesktopBtn:".close-sm",
        reviewForm:"#form-review",
        confirmationMessage:".review-preview",
        previewButton: "#preview-button",
        nameInput:"#id_name",
        emailInput:"#id_email",
        titleInput:"#id_title",
        reviewInput:"#id_review",
        errors: ".error",
        yesButton: ".yes-btn",
        cancelButton: ".cancel-btn",
        confirmationMessageContent:".review-preview-content",
        confirmCloseBtn: ".fa-close",
        stepsBtn: "#step-by-step",
        videoBtn: "#videoBtn",
        videoContainer: ".video-container",
        stepsContainer: ".steps-container",
        relatedRecipesSlider: ".js-related-recipes-slider",
        fbShareBtn: ".js-fb-share",
        buyNow: ".js-buy-now"
    }
})
export default class ViewController extends Marionette.View<Backbone.Model>{
    constructor() {
        super();
    }

    initialize(){
        this.addEventListeners();
        this.initializeRelatedRecipesSlider();
    }
    addEventListeners() {
        this.ui.reviewsLink.on('click', this.onReviewsClick.bind(this));
        this.ui.reviewsTab.on('click',this.onReviewsTabClick.bind(this));
        this.ui.dropDown.on('click',this.onDropDownClick.bind(this));
        this.ui.dropDownOptions.children().on('click',this.onDropDownOptionClick.bind(this));
        $( document ).on('click',this.onOutsideDropDownClick.bind(this));
        this.ui.writeReviewBtn.on('click',this.onWriteReviewBtnClick.bind(this));
        this.ui.closeModalBtn.on('click',this.onModalClose.bind(this));
        this.ui.closeModalDesktopBtn.on('click',this.onModalClose.bind(this));
        this.ui.previewButton.on('click',this.onPreviewButtonClick.bind(this));
        this.ui.yesButton.on('click',this.onYesButtonClick.bind(this));
        this.ui.cancelButton.on('click',this.onCancelButtonClick.bind(this));
        this.ui.confirmCloseBtn.on('click',this.onConfirmCloseBtnClick.bind(this));
        this.ui.stepsBtn.on('click',this.onStepsBtnClick.bind(this));
        this.ui.videoBtn.on('click',this.onVideoBtnClick.bind(this));
        this.ui.fbShareBtn.on('click', this.onFbShareClick.bind(this));
        this.ui.buyNow.on("click", this.onWhereToBuyClick);
    }

    onReviewsClick(ev) {
        this.ui.tabs.addClass('slide');
        this.ui.reviewsTab.removeClass("active");
        $('.tab-reviews').addClass('active');
        this.ui.instructionsContent.fadeOut();
        this.ui.reviewsContent.fadeIn();

        $("html, body").animate(
            {
                scrollTop: $('.instructions-reviews').offset().top - 100,
            },
            1000
        );
    }

    onReviewsTabClick(ev){
        var target = $(ev.currentTarget);

        if(target.attr("rel") == "reviews"){
            this.ui.tabs.addClass('slide');
            this.ui.instructionsContent.fadeOut();
            this.ui.reviewsContent.fadeIn();
            if (window['player'].hasOwnProperty('pauseVideo')){
                window['player'].pauseVideo();
            }

        }else{
            this.ui.tabs.removeClass('slide');
            this.ui.reviewsContent.fadeOut();
            this.ui.instructionsContent.fadeIn();
        }
        this.ui.reviewsTab.removeClass("active");
        target.addClass("active");

    }

    onStepsBtnClick(){
        if (this.ui.stepsBtn.hasClass("hided")){
            this.ui.videoContainer.css('display', 'none');
            this.ui.stepsContainer.css('display', 'block');
            window['player'].pauseVideo();
            this.ui.videoBtn.toggleClass("showed");
            this.ui.stepsBtn.toggleClass("showed");
            this.ui.videoBtn.toggleClass("hided");
            this.ui.stepsBtn.toggleClass("hided");
        }
    }

    onVideoBtnClick(){
        if (this.ui.videoBtn.hasClass("hided")){
            this.ui.videoContainer.css('display', 'block');
            this.ui.stepsContainer.css('display', 'none');
            this.ui.videoBtn.toggleClass("showed");
            this.ui.stepsBtn.toggleClass("showed");
            this.ui.videoBtn.toggleClass("hided");
            this.ui.stepsBtn.toggleClass("hided");
        }
    }

    onDropDownClick(){
        this.ui.dropDownOptions.toggleClass("select-hide");
    }

    onDropDownOptionClick(e){
        this.ui.dropDown.html($(e.currentTarget).text());
        this.ui.dropDownOptions.toggleClass("select-hide");
        this.ui.dropDownOptions.children(".same-as-selected").removeClass("same-as-selected");
        $(e.currentTarget).addClass("same-as-selected");
    }

    onOutsideDropDownClick(elmnt){
        if(this.ui.dropDown[0] === elmnt.target){
            return;
        }
        this.ui.dropDownOptions.addClass("select-hide");
    }

    onWriteReviewBtnClick(){
        this.ui.reviewsModal.addClass("visible");
    }

    onPreviewButtonClick(event){
        this.ui.errors[0].innerHTML="";
        this.ui.errors[1].innerHTML="";
        this.ui.errors[2].innerHTML="";
        this.ui.errors[3].innerHTML="";

        if(this.ui.nameInput[0].validity.valid
            && this.ui.emailInput[0].validity.valid
            && this.ui.titleInput[0].validity.valid
            && this.ui.reviewInput[0].validity.valid){
                let starRate='';
                for(let i=0;i<this.$('.star-rating-input:checked').val();i++){
                    starRate +='<i class="fa fa-star fa-1x"></i>';
                }
                this.ui.confirmationMessageContent[0].innerHTML = '<br><span>Rate: </span><span>'+
                starRate + '</span><br><span>Review: </span><p>'+this.ui.reviewInput[0].value+'</p>';
                this.ui.confirmationMessage.addClass('visible')
        }

        if(!this.ui.nameInput[0].validity.valid){
            this.ui.errors[0].innerHTML=" a valid name is required";
        }

        if(!this.ui.emailInput[0].validity.valid){
            this.ui.errors[1].innerHTML=" a valid email is required";
        }

        if(!this.ui.titleInput[0].validity.valid){
            this.ui.errors[2].innerHTML=" a valid review title is required";
        }

        if(!this.ui.reviewInput[0].validity.valid){
            this.ui.errors[3].innerHTML=" a not empty review is required";
        }
    }

    onYesButtonClick(){
        this.ui.reviewForm[0].submit();
        this.ui.confirmationMessage.removeClass('visible');
    }

    onCancelButtonClick(){
        this.ui.confirmationMessage.removeClass('visible');
    }

    onConfirmCloseBtnClick(){
        this.ui.confirmationMessage.removeClass('visible');
    }
    onModalClose(){
        this.ui.reviewsModal.removeClass('visible');
        this.ui.confirmationMessage.removeClass('visible');
    }

    onFbShareClick(ev) {
        var url = $(ev.currentTarget).data('url');
        window["FB"].ui({
            method: 'share',
            href: url,
        }, function(response){});
    }

    onWhereToBuyClick(ev) {
        var $this = $(this);
        var container = $this.attr("data-destini-container");
        var association = $this.attr("data-destini-association");
        window["destini"].init(container);
        window["destini"].loadWidget(association);
    }    

    initializeRelatedRecipesSlider() {
        let options = {
            slidesToShow: 1.05,
            infinite: false,
            arrows: false,
            mobileFirst: true,
            swipeToSlide: true,
            responsive: [
                {
                    breakpoint: 760,
                    settings: {
                        slidesToShow: 2,
                        slidesToSwipe: 2
                    }
                },
                {
                    breakpoint: 1023,
                    settings: {
                        slidesToShow: 3,
                        slidesToSwipe: 1
                    }
                }, 
                {
                    breakpoint: 1024,
                    settings: {
                        slidesToShow: 4,
                        slidesToSwipe: 1
                    }
                }
            ]
        }

        this.ui.relatedRecipesSlider.slick(options);
    }

    onRender() {
    }
}
