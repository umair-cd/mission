from django import forms

from . import models


class DynamicCampaignHeroImageForm(forms.ModelForm):
    class Meta:
        model = models.DynamicCampaignHeroImage
        fields = '__all__'

        labels = {
            'cta_button_label': 'CTA text',
            'cta_button_link': 'CTA link'
        }


class DynamicCampaignHighlightedProductForm(forms.ModelForm):
    class Meta:
        model = models.DynamicCampaignHighlightedProduct
        fields = '__all__'

        labels = {
            'link_label': 'CTA text'
        }


class DynamicCampaignAdditionalProductForm(forms.ModelForm):
    class Meta:
        model = models.DynamicCampaignAdditionalProduct
        fields = '__all__'

        labels = {
            'cta_label': 'CTA text'
        }


class DynamicCampaignInfluencerForm(forms.ModelForm):
    class Meta:
        model = models.DynamicCampaignInfluencer
        fields = '__all__'

        labels = {
            'blog_title': 'Eyebrow title',
            'button_label': 'CTA text',
            'button_link': 'CTA link'
        }


class DynamicCampaignPageForm(forms.ModelForm):
    class Meta:
        model = models.DynamicCampaignPage
        fields = '__all__'
        labels = {
            'recipes_section_button_label': 'Recipe section CTA text',
            'recipes_section_button_link': 'Recipe section CTA link'
        }
        help_texts = {
            'title': 'Internal name for campaign (only visible in admin)'
        }


class ReviewForm(forms.Form):
    name = forms.CharField(
        label='Name:',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'your name',
                'pattern': '.*\S+.*'
            }
        )
    )

    email = forms.EmailField(
        label='Email:',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'your email',
                'type': "email"
            }
        )
    )

    title = forms.CharField(
        label='Title:',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'review title',
                'pattern': '.*\S+.*'
                }
        )
    )

    review = forms.CharField(
        label='Review:',
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'cols': 50
            }
        )
    )

    STAR_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )

    rate = forms.ChoiceField(
        label='Rate:',
        choices=STAR_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'fa fa-star star-rate'})
    )
