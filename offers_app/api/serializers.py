from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from profile_app.models import CustomerProfile, BusinessProfile
from upload_app.models import FileUpload


def get_image_url(offer):
    """
    Return the file URL for an offer's uploaded image, or None.
    """
    
    if offer.image and offer.image.file:
        return offer.image.file.url
    return None

class ProfileUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating user profile fields (first_name, last_name)
    within an offer update request.
    """

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

class OfferDetailListSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for listing offer details with their URL.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        read_only_fields = ['id', 'url']

    def get_url(self, obj):
        """Return the detail URL for the given offer detail."""
        return f"/offerdetails/{obj.id}/"


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating offer detail entries.
    Features are accepted as a list of strings.
    """

    features = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'offer_type': {'required': True},
        }

class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating offers with nested offer details.
    Requires at least three detail entries.
    """

    details = OfferDetailCreateSerializer(source='offer_details', many=True)
    image = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details'
        ]
        read_only_fields = ['id']

    def validate_details(self, value):
        """
        Validate that the 'details' list contains at least three items.
        """
        
        if len(value) < 3:
            raise serializers.ValidationError("At least three offer details are required.")
        return value

    def create(self, validated_data):
        """
        Create an offer with nested details and calculate price/delivery aggregates.
        """

        details_data = validated_data.pop('offer_details', [])
        uploaded_file = validated_data.pop('image', None)

        if uploaded_file:
            file_upload = FileUpload.objects.create(file=uploaded_file)
            validated_data['image'] = file_upload

        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            features = detail_data.pop('features', [])
            offer_detail = OfferDetail.objects.create(offer=offer, **detail_data)
            offer_detail.features = features
            offer_detail.save()

        if offer.offer_details.exists():
            offer.min_price = min((detail.price for detail in offer.offer_details.all() if detail.price), default=None)
            offer.min_delivery_time = min((detail.delivery_time_in_days for detail in offer.offer_details.all() if detail.delivery_time_in_days), default=None)
            offer.save()

        return offer

class UserDetailsSerializer(serializers.Serializer):
    """
    Read-only serializer for embedding basic user information in offer responses.
    """

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()

class OfferListSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for listing offers with nested details and user information.
    """

    details = OfferDetailListSerializer(source='offer_details', many=True, read_only=True)
    user_details = UserDetailsSerializer(source='user', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'min_price',
            'min_delivery_time',
            'user_details',
            'details'
        ]

    def get_image(self, obj):
        """Return the file URL for the offer's image, or None."""
        return get_image_url(obj)


class SingleOfferSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for retrieving a single offer with nested details and user information.
    """

    details = OfferDetailListSerializer(source='offer_details', many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'min_price',
            'min_delivery_time',
            'details'
        ]

    def get_image(self, obj):
        """Return the file URL for the offer's image, or None."""
        return get_image_url(obj)

class SingleOfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an offer with nested offer details.
    Supports partial updates of top-level fields and nested details.
    """

    details = OfferDetailCreateSerializer(source='offer_details', many=True, required=False)
    user_details = ProfileUpdateSerializer(required=False)
    image = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details',
            'user_details'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
        }

    def validate(self, attrs):
        """Ensure each detail entry includes the required 'offer_type' field."""
        details_data = self.initial_data.get('details')
        if details_data:
            for detail in details_data:
                if 'offer_type' not in detail:
                    raise serializers.ValidationError(
                        {"details": ["Each detail entry must include the 'offer_type' field."]}
                    )
        return attrs

    def to_representation(self, instance):
        """
        Use SingleOfferSerializer for output, excluding user, min_price, min_delivery_time,
        created_at and updated_at. Details are shown with full fields including offer_type.
        """

        representation = SingleOfferSerializer(instance).data
        representation.pop('user', None)
        representation.pop('min_price', None)
        representation.pop('min_delivery_time', None)
        representation.pop('created_at', None)
        representation.pop('updated_at', None)
        representation['details'] = OfferDetailCreateSerializer(instance.offer_details.all(), many=True).data
        return representation

    def _update_offer_fields(self, instance, validated_data):
        """
        Update top-level offer fields, excluding nested offer_details.
        Handles file upload for the image field.
        """

        uploaded_file = validated_data.pop('image', None)
        if uploaded_file:
            file_upload = FileUpload.objects.create(file=uploaded_file)
            instance.image = file_upload

        for attr, value in validated_data.items():
            if attr != 'offer_details':
                setattr(instance, attr, value)
        instance.save()

    def _update_or_create_details(self, instance, details_data):
        """
        Update existing offer details matched by offer_type.
        Only provided fields are updated; others remain unchanged.
        """
        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            if offer_type:
                try:
                    detail = instance.offer_details.get(offer_type=offer_type)
                    for attr, value in detail_data.items():
                        setattr(detail, attr, value)
                    detail.save()
                except OfferDetail.DoesNotExist:
                    OfferDetail.objects.create(offer=instance, **detail_data)

    def _recalculate_aggregates(self, instance):
        """
        Recalculate min_price and min_delivery_time from all offer details.
        """
        details = instance.offer_details.all()
        instance.min_price = min((d.price for d in details if d.price), default=None)
        instance.min_delivery_time = min((d.delivery_time_in_days for d in details if d.delivery_time_in_days), default=None)
        instance.save()

    def update(self, instance, validated_data):
        """
        Update offer fields and nested offer details, then recalculate aggregates.
        """
        self._update_offer_fields(instance, validated_data)
        details_data = validated_data.get('offer_details')
        if details_data:
            self._update_or_create_details(instance, details_data)
            self._recalculate_aggregates(instance)
        return instance

class SingleOfferDeleteSerializer(serializers.ModelSerializer):
    """
    Empty serializer used for deleting an offer.
    """

    class Meta:
        model = Offer
        fields = []

class SingleOfferDetailSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for retrieving a single offer detail entry.
    """

    class Meta:
        model = OfferDetail
        fields = [
            'id', 
            'title', 
            'revisions', 
            'delivery_time_in_days', 
            'price', 
            'features', 
            'offer_type'
        ]