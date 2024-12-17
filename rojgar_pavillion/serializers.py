from rest_framework import serializers
from .models import Registration, Participant, TrainingSession

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        exclude = ['registration', 'is_free_entry']

class RegistrationSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)
    
    class Meta:
        model = Registration
        fields = [
            'id', 'training_session', 'registration_type',
            'total_price', 'payment_method', 'payment_screenshot',
            'agreed_to_no_refund', 'is_early_bird', 'is_expo_access',
            'created_at', 'participants'
        ]
        read_only_fields = [
            'registration_type', 'total_price', 'is_early_bird',
            'is_expo_access', 'created_at'
        ]

    def validate(self, data):
        if not data.get('agreed_to_no_refund'):
            raise serializers.ValidationError(
                "You must agree to the no-refund policy"
            )

        participants = data.get('participants', [])
        if not participants:
            raise serializers.ValidationError(
                "At least one participant is required"
            )

        # Validate training session availability
        training_session = data['training_session']
        if not training_session.is_available():
            raise serializers.ValidationError(
                "This training session is full"
            )

        if (training_session.current_participants + len(participants) > 
            training_session.time_slot.max_participants):
            raise serializers.ValidationError(
                "Not enough spots available in this session"
            )

        return data

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        
        # Determine registration type
        if len(participants_data) == 6:
            validated_data['registration_type'] = 'GROUP'
        elif validated_data.get('is_expo_access'):
            validated_data['registration_type'] = 'EXPO_ACCESS'
        else:
            validated_data['registration_type'] = 'SINGLE'

        validated_data['total_participants'] = len(participants_data)

        
        registration = Registration.objects.create(**validated_data)

        # Create participants
        for idx, participant_data in enumerate(participants_data):
            is_free = (len(participants_data) == 6 and idx == 5)
            Participant.objects.create(
                registration=registration,
                is_free_entry=is_free,
                **participant_data
            )

        return registration