from rest_framework import serializers
from .models import Registration, TimeSlot, Topic
from django.utils import timezone

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            'id', 'time_slot', 'registration_type', 'status',
            'first_name', 'last_name', 'qualification', 'gender', 'age',
            'address', 'mobile_number', 'email',
            'total_participants', 'total_price', 'payment_method',
            'payment_screenshot', 
            'agreed_to_no_refund', 'is_early_bird', 'is_expo_access',
            'is_free_entry',
            'qr_code',
            'created_at', 'updated_at',
            'group_members',
            'registration_type',
            'is_attended'
        ]
        read_only_fields = [
            'total_price', 'is_early_bird',
            'is_expo_access', 'status', 'qr_code', 'created_at',
            'updated_at'
        ]

    def validate(self, data):
        data = super().validate(data)
        
        if not data.get('agreed_to_no_refund'):
            raise serializers.ValidationError(
                "You must agree to the no-refund policy"
            )

        time_slot = data['time_slot']
        
        # Check if the event date has passed
        if time_slot.topic.start_date < timezone.now().date():
            raise serializers.ValidationError(
                "Cannot register for past events"
            )

        # Check if the topic is active
        if not time_slot.topic.is_active:
            raise serializers.ValidationError(
                "This event is no longer accepting registrations"
            )

        # Check time slot availability
        if not time_slot.is_available():
            raise serializers.ValidationError(
                "This time slot is full"
            )

        if (time_slot.current_participants + data['total_participants'] > 
            time_slot.max_participants):
            raise serializers.ValidationError(
                "Not enough spots available in this time slot"
            )

        # Validate group_members if registration type is GROUP
        if data['registration_type'] == 'Group':
            group_members = data.get('group_members')
            if not group_members:
                raise serializers.ValidationError(
                    "Group members information is required for group registrations"
                )
            # Ensure group_members is a valid JSON structure
            if not isinstance(group_members, list):
                raise serializers.ValidationError(
                    "Group members must be a list"
                )
            # Additional validation for each member can be added here
            for member in group_members:
                if not isinstance(member, dict):
                    raise serializers.ValidationError(
                        "Each group member must be a dictionary"
                    )
                # Example validation for required fields in each member
                if 'name' not in member or 'email' not in member:
                    raise serializers.ValidationError(
                        "Each group member must have a 'name' and 'email'"
                    )

        return data

class TopicSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'description']

class TimeSlotSmallSerializer(serializers.ModelSerializer):
    topic = TopicSmallSerializer()
    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'end_time', 'date', 'topic']

class RegistrationDetailSerializer(serializers.ModelSerializer):
    time_slot = TimeSlotSmallSerializer()
    class Meta:
        model = Registration
        fields = '__all__'

class TimeSlotSerializer(serializers.ModelSerializer):
    available_spots = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = TimeSlot
        fields = [
            'id', 'topic', 'start_time', 'end_time',
            'max_participants', 'current_participants',
            'available_spots','date'
        ]

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            'id', 'name', 'description', 'start_date',
            'end_date', 'venue', 'is_active','image'
        ]