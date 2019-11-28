import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as $ from "jquery";
import * as _ from "underscore";
import { on, Options } from "../utils/decorators";

/**
 * This controller is a good spot to initialize any javascript comonents
 * that might need setup for demo in the UI Docs.
 */

@Options({
    template: false,
    el: "body",
    ui: {
        navbar: ".navbar",
        hamburger: ".js-hamburger",
        isActive: ".is-active",
        mobileNav: "#mobile-navbar",
        mobileNavButtonClose: "#mobile-navbar > .closebtn",
        recipesLink: "#recipes-link",
        productsLink: "#products-link",
        aboutUsLink: "#about-us-link",
        recipesNav: "#recipes-nav",
        aboutUsNav: "#about-us-nav",
        aboutUsNavButtonClose: "#about-us-nav > .closebtn",
        aboutUsNavButtonBack: "#about-us-nav > .back",
        recipesNavButtonClose: "#recipes-nav > .closebtn",
        recipesNavButtonBack: "#recipes-nav > .back",
        productsNav: "#products-nav",
        productsNavButtonClose: "#products-nav > .closebtn",
        productsNavButtonBack: "#products-nav > .back",
        productsNavTitle: "#products-nav h3",
        productCategory: "#products-nav .product-category",
        productCategoryButton: "#products-nav .product-category-button",
        productCategoryLink: "#products-nav .product-category-link",
        recipesContent: ".recipes-content",
        aboutContent: ".about-content",
        desktopRecipesLink: "#desktop-recipes-link",
        desktopAboutLink: "#desktop-about-link",
        productsContent: ".products-content",
        desktopProductsLink: "#desktop-products-link",
        desktopSearchButton: "#desktopSearchButton",
        searchContent: ".search-content",
        searchSelector: ".searchSelector",
        searchInput: ".searchInput",
        searchButton: ".searchButton",
        mobileSearchButton: "#searchButtonMobile",
        mobileSearchContainer: ".search-container-mobile",
        socialLinksContainer: "#socialLinksContainer",
        animateOnScroll: ".animation-scroll-activated",
        openImageModal: ".js-open-image-modal",
        imageModal: ".js-image-modal",
        shareModal: ".js-share-modal",
        closeModal: ".js-close-modal",
        recipeCardShareIcon: ".recipe-card-share-icon",
        copyLinkInput: "#copy-link-input",
        shareModalCopyLink: ".js-share-modal .copy-link",
        resultsTitle: ".js-results-title",
        shareModalTwitter: ".js-share-modal .js-share-twitter",
        shareModalPinterest: ".js-share-modal .js-share-pinterest",
        shareModalEmail: ".js-share-modal .js-share-email",
        shareModalFacebook: ".js-share-modal .js-share-facebook",
        copyLink: ".copy-link",
        grid: ".grid", 
        searchForm: ".search-form-filter-fields"
    }
})
export default class ViewController extends Marionette.View<Backbone.Model> {
    isHomepage = $("body").hasClass("home-page");
    recipesClicked = false;
    productsClicked = false;
    aboutClicked = false;

    constructor() {
        super();

        this.isHomepage && this.ui.navbar.addClass("transparent");
    }

    initialize() {
        this.initAnimations();

        var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(
            navigator.userAgent
        )
            ? true
            : false;

        //achor to section on search page
        if (/[?&]q=/.test(location.search) && !isMobile) {
            $("html, body").animate(
                { scrollTop: this.ui.searchForm.offset().top - 50},
                1000
            );
        }

        if (/[?&]q=/.test(location.search) && isMobile) {
            $("html, body").animate(
                { scrollTop: this.ui.searchForm.offset().top + 200},
                1000
            );
        }

    }

    initHistoryAnimations() {
        const points = this.ui.animateOnScroll;
        this.ui.animateOnScroll.waypoint({
            offset: "80%",
            handler: function(direction) {
                const $el = $(this.element);
                const $prev = $el.prev(".animation-scroll-activated");
                if (direction === "down") {
                    $el.removeClass("animation-active");
                    $prev.addClass("animation-active");
                }
            }
        });
        this.ui.animateOnScroll.waypoint({
            offset: "100%",
            handler: function(direction) {
                if (direction === "up") {
                    points.removeClass("animation-active");
                }
            }
        });
    }

    initAnimations() {
        // diff animations for Our History page
        if ($("body").hasClass("our-history")) {
            this.initHistoryAnimations();
        } else {
            this.ui.animateOnScroll.waypoint({
                offset: "80%",
                handler: function(direction) {
                    if (direction === "down") {
                        $(this.element).addClass("animation-active");
                    }
                }
            });
        }
    }

    onRender() {
        // Temp
    }

    @on("click @ui.productCategory")
    onProductCategoryClick(e) {
        var $category = $(e.currentTarget);
        $category.addClass("selected-category");
        this.ui.productCategoryButton.hide();
        this.ui.productsNavTitle.hide();
    }

    @on("click @ui.hamburger")
    onHamburgerClick(JQueryEventObject: any) {
        this.ui.mobileNav.css("width", "100%");
        this.ui.hamburger.toggleClass("is-active");
        this.ui.navbar.toggleClass("mobile-nav-expanded");
    }

    @on("click @ui.mobileNavButtonClose")
    onMobileNavButtonCloseClick(JQueryEventObject: any) {
        this.ui.mobileNav.css("width", "0%");
        this.ui.navbar.toggleClass("mobile-nav-expanded");
        this.ui.productCategory.removeClass("selected-category");
    }

    @on("click @ui.recipesLink")
    onRecipesLinkClick(JQueryEventObject: any) {
        this.ui.mobileNav.css("width", "0%");
        this.ui.recipesNav.css("width", "100%");
    }

    @on("click @ui.recipesNavButtonClose")
    onRecipesButtonCloseClick(JQueryEventObject: any) {
        this.ui.mobileNav.css("width", "0%");
        this.ui.recipesNav.css("width", "0%");
        this.ui.navbar.toggleClass("mobile-nav-expanded");
    }

    @on("click @ui.recipesNavButtonBack")
    onRecipesButtonBackClick(JQueryEventObject: any) {
        this.ui.mobileNav.css("width", "100%");
        this.ui.recipesNav.css("width", "0%");
    }
    @on("click @ui.productsLink")
    onProductsLinkClick(JQueryEventObject: any) {
        this.ui.mobileNav.css("width", "0%");
        this.ui.productsNav.css("width", "100%");
        this.ui.productCategoryButton.show();
        this.ui.productCategoryLink.hide();
    }

    @on("click @ui.productsNavButtonClose")
    onProductsButtonCloseClick(JQueryEventObject: any) {
        this.ui.mobileNav.css("width", "0%");
        this.ui.productsNav.css("width", "0%");
        this.ui.navbar.toggleClass("mobile-nav-expanded");
        this.ui.productCategory.removeClass("selected-category");
        this.ui.productsNavTitle.show();
    }

    @on("click @ui.productsNavButtonBack")
    onProductsButtonBackClick(JQueryEventObject: any) {
        this.ui.mobileNav.css("width", "100%");
        this.ui.productsNav.css("width", "0%");
        this.ui.productCategory.removeClass("selected-category");
        this.ui.productsNavTitle.show();
    }

    @on("click @ui.aboutUsLink")
    onAboutUsLinkClick(JQueryEventObject: any) {
        this.ui.mobileNav.css("width", "0%");
        this.ui.aboutUsNav.css("width", "100%");
    }

    @on("click @ui.aboutUsNavButtonClose")
    onAboutUsButtonCloseClick(JQueryEventObject: any) {
        this.ui.mobileNav.css("width", "0%");
        this.ui.aboutUsNav.css("width", "0%");
        this.ui.navbar.toggleClass("mobile-nav-expanded");
    }

    @on("click @ui.aboutUsNavButtonBack")
    onAboutUsButtonBackClick(JQueryEventObject: any) {
        this.ui.mobileNav.css("width", "100%");
        this.ui.aboutUsNav.css("width", "0%");
    }

    @on("click @ui.desktopRecipesLink")
    onDesktopRecipesLinkClick(JQueryEventObject: any) {
        this.recipesClicked = !this.recipesClicked;
        this.productsClicked = false;
        this.aboutClicked = false;
    }

    @on("mouseenter @ui.desktopRecipesLink")
    @on("mouseleave @ui.recipesContent")
    onDesktopRecipesLinkMouse(JQueryEventObject: any) {
        if (
            this.ui.recipesContent.css("display") === "block" &&
            !this.recipesClicked
        ) {
            this.ui.recipesContent.css("display", "none");
            if (this.isHomepage && !this.ui.navbar.hasClass("is-fixed")) {
                this.ui.navbar.addClass("transparent");
            }
        } else {
            this.ui.recipesContent.css("display", "block");
            this.isHomepage && this.ui.navbar.removeClass("transparent");
        }
        this.ui.productsContent.css("display", "none");
        this.ui.searchContent.css("display", "none");
        this.ui.aboutContent.css("display", "none");
        this.productsClicked = false;
        this.aboutClicked = false;
    }

    @on("click @ui.desktopProductsLink")
    onDesktopProductsLinkClick(JQueryEventObject: any) {
        this.productsClicked = !this.productsClicked;
        this.recipesClicked = false;
        this.aboutClicked = false;
    }

    @on("mouseenter @ui.desktopProductsLink")
    @on("mouseleave @ui.productsContent")
    onDesktopProductsLinkMouse(JQueryEventObject: any) {
        if (
            this.ui.productsContent.css("display") === "block" &&
            !this.productsClicked
        ) {
            this.ui.productsContent.css("display", "none");
            if (this.isHomepage && !this.ui.navbar.hasClass("is-fixed")) {
                this.ui.navbar.addClass("transparent");
            }
        } else {
            this.ui.productsContent.css("display", "block");
            this.isHomepage && this.ui.navbar.removeClass("transparent");
        }
        this.ui.recipesContent.css("display", "none");
        this.ui.searchContent.css("display", "none");
        this.ui.aboutContent.css("display", "none");
        this.recipesClicked = false;
        this.aboutClicked = false;
    }

    @on("click @ui.desktopAboutLink")
    desktopAboutLinkClick(JQueryEventObject: any) {
        this.aboutClicked = !this.aboutClicked;
        this.productsClicked = false;
        this.recipesClicked = false;
    }

    @on("mouseenter @ui.desktopAboutLink")
    @on("mouseleave @ui.aboutContent")
    desktopAboutLinkLinkMouse(JQueryEventObject: any) {
        if (
            this.ui.aboutContent.css("display") === "block" &&
            !this.aboutClicked
        ) {
            this.ui.aboutContent.css("display", "none");
            if (this.isHomepage && !this.ui.navbar.hasClass("is-fixed")) {
                this.ui.navbar.addClass("transparent");
            }
        } else {
            this.ui.aboutContent.css("display", "block");
            this.isHomepage && this.ui.navbar.removeClass("transparent");
        }
        this.ui.recipesContent.css("display", "none");
        this.ui.productsContent.css("display", "none");
        this.ui.searchContent.css("display", "none");
        this.productsClicked = false;
    }

    @on("click @ui.desktopSearchButton")
    onDesktopSearchButton(JQueryEventObject: any) {
        if (this.ui.searchContent.css("display") === "block") {
            this.ui.searchContent.css("display", "none");
            if (this.isHomepage && !this.ui.navbar.hasClass("is-fixed")) {
                this.ui.navbar.addClass("transparent");
            }
        } else {
            this.ui.searchContent.css("display", "block");
            this.isHomepage && this.ui.navbar.removeClass("transparent");
        }
        this.ui.productsContent.css("display", "none");
        this.ui.recipesContent.css("display", "none");
    }
    @on("change @ui.searchSelector")
    onSearchSelectorOnchange(JQueryEventObject: any) {
        this.ui.searchInput.attr(
            "placeholder",
            `Type to search ${JQueryEventObject.target.value.toLowerCase()}`
        );
    }

    @on("click @ui.mobileSearchButton")
    onMobileSearchButton(JQueryEventObject: any) {
        if (this.ui.mobileSearchContainer.css("display") === "block") {
            this.ui.mobileSearchContainer.css("display", "none");
            this.ui.socialLinksContainer.css("display", "block");
        } else {
            this.ui.mobileSearchContainer.css("display", "block");
            this.ui.socialLinksContainer.css("display", "none");
        }
    }

    @on("click @ui.openImageModal")
    onOpenImageModal(event) {
        var imageURL = $(event.currentTarget).data("src");
        this.ui.imageModal.find(".js-image-target").attr("src", imageURL);
        this.ui.imageModal.addClass("visible");
        event.preventDefault();
    }

    @on("click @ui.closeModal")
    oncloseImageModal(event) {
        this.ui.imageModal.removeClass("visible");
        this.ui.shareModal.removeClass("visible");
        var copyBtnText = this.ui.copyLink.text();
        this.ui.copyLinkInput.css("background-color", "#7f7f7f40");
        this.ui.copyLinkInput.css("color", "#333333");
        this.ui.copyLink.text(copyBtnText.replace('Link Copied', 'Copy Link'));
        this.ui.copyLink.css("color", "#da291c");
    }

    @on("click @ui.recipeCardShareIcon")
    onClickRecipeCardShareIcon(event) {
        event.preventDefault();
        var recipe = $(event.currentTarget).data();
        this.ui.shareModal.addClass("visible");
        this.ui.copyLinkInput.val(
            window.location.origin +
                $(event.currentTarget)
                    .prev("a")
                    .attr("href")
        );

        this.ui.shareModalFacebook.attr("data-url", recipe.url);

        this.ui.shareModalTwitter.attr(
            "href",
            this.buildTwitterShare(recipe.title, recipe.url)
        );
        this.ui.shareModalPinterest.attr(
            "href",
            this.buildPinterestShare(
                recipe.url,
                recipe.imageUrl,
                recipe.description
            )
        );
        this.ui.shareModalEmail.attr(
            "href",
            this.buildEmailShare(recipe.url, recipe.title, recipe.featuredTitle)
        );
    }

    @on("click @ui.shareModalCopyLink")
    onClickShareModalCopyLink() {
        var $input = this.ui.copyLinkInput;
        if (navigator.userAgent.match(/ipad|ipod|iphone/i)) {
            var el = $input.get(0);
            var editable = el.contentEditable;
            var readOnly = el.readOnly;
            el.contentEditable = true;
            el.readOnly = false;
            var range = document.createRange();
            range.selectNodeContents(el);
            var sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
            el.setSelectionRange(0, 999999);
            el.contentEditable = editable;
            el.readOnly = readOnly;
        } else {
            $input.select();
        }
        document.execCommand("copy");
        $input.blur();
    }

    @on("click @ui.copyLink")onClickCopyLink(){
        console.log("copied link");
        var copyBtnText = this.ui.copyLink.text();
        this.ui.copyLinkInput.css("background-color", "#da291c");
        this.ui.copyLinkInput.css("color", "white");
        this.ui.copyLink.text(copyBtnText.replace('Copy Link', 'Link Copied'));
        this.ui.copyLink.css("color", "gray");

    }

    buildTwitterShare(title, url) {
        return "https://twitter.com/intent/tweet?text=" + title + "— " +  url;
    }

    buildPinterestShare(url, media, description) {
        return (
            "https://pinterest.com/pin/create/button?url=" +
            url +
            "&media=" +
            media +
            "&description=" +
            description
        );
    }

    buildEmailShare(url, title, featuredTitle) {
        return (
            "mailto:?subject=Thought you’d love this " +
            title +
            " using " +
            featuredTitle +
            ".&body=" +
            url
        );
    }

   @on("click @ui.shareModalFacebook")
    onShareModalFacebook(event) {
        var url = $(event.currentTarget).data("url");
        window["FB"].ui({
            method: 'share',
            href: url,
        }, function(response){});
    }
}
