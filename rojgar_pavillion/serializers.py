from rest_framework import serializers
from .models import Registration, TimeSlot, Topic
from django.utils import timezone

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            'id', 'time_slot', 'registration_type', 'status',
            # Participant Info
            'full_name', 'qualification', 'gender', 'age',
            'address', 'mobile_number', 'email',
            # Payment and Status
            'total_participants', 'total_price', 'payment_method',
            'payment_screenshot', 
            # Flags
            'agreed_to_no_refund', 'is_early_bird', 'is_expo_access',
            'is_free_entry',
            # QR Code
            'qr_code',
            # Timestamps
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'registration_type', 'total_price', 'is_early_bird',
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

        return data

class TimeSlotSerializer(serializers.ModelSerializer):
    available_spots = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = TimeSlot
        fields = [
            'id', 'topic', 'start_time', 'end_time',
            'max_participants', 'current_participants',
            'available_spots'
        ]

class TopicSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, read_only=True)
    
    class Meta:
        model = Topic
        fields = [
            'id', 'name', 'description', 'start_date',
            'end_date', 'venue', 'is_active', 'time_slots'
        ]