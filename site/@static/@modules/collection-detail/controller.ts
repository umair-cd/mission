import * as Backbone from "backbone";
import * as Marionette from "backbone.marionette";
import * as _ from "underscore";
import {on, Options} from "../utils/decorators";


@Options({
    template: false,
    el: "body",
    ui: {
        loadMoreButtons:".load-more",
        recipeCards: ".collection-recipes ul.grid li"
    }
})
export default class ViewController extends Marionette.View<Backbone.Model>{
    start = 8;
    increment = 8;
    cardsLength = this.ui.recipeCards.length;

    constructor() {
        super();
    }

    initialize() {
        this.ui.loadMoreButtons.on('click',this.onLoadMoreClick.bind(this));
        this.hideCards();
    }

    hideCards() {
        this.ui.recipeCards.slice(8, this.cardsLength).addClass('hidden');
    }

    onLoadMoreClick(e){
        this.ui.recipeCards.slice(this.start, this.start + this.increment).removeClass('hidden');
        this.start += this.increment;
        this.checkIfMore();
    }

    checkIfMore() {
        if (this.cardsLength <= this.start) {
            this.ui.loadMoreButtons.hide();
        }
    }

    onRender() {
        this.checkIfMore();
        console.log("Collection Detail ViewController Rendered!");
    }
}
