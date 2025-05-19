from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from .models import Aircraft
from .serializers import AircraftSerializer
from .forms import AircraftAssembleForm 
from django.contrib import messages
from django.db.models import F
from parts.models import Part

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def aircraft_list(request):
    user_team = request.user.profile.team 
    aircrafts = Aircraft.objects.filter(assembled_by__profile__team=user_team)
    return render(request, 'aircrafts/aircraft_list.html', {'aircrafts': aircrafts})

@login_required
def aircraft_assemble(request):
    team = request.user.profile.team

    if request.method == 'POST':
        form = AircraftAssembleForm(request.POST, team=team)

        if form.is_valid():
            selected_parts = form.cleaned_data['parts']

            # Validate part combination
            required_types = {'Fuselage': 1, 'Engine': 1, 'Wing': 2}
            part_type_counts = {ptype: 0 for ptype in required_types}

            for part in selected_parts:
                part_type_counts[part.part_type] += 1

            # Check constraints
            for ptype, required in required_types.items():
                if part_type_counts[ptype] != required:
                    messages.error(request, f"You need exactly {required} {ptype}(s).")
                    return render(request, 'aircrafts/aircraft_assemble.html', {'form': form})

            # Create the aircraft
            aircraft = Aircraft.objects.create(team=team)
            aircraft.parts.set(selected_parts)

            # Mark parts as used (if applicable)
            for part in selected_parts:
                part.used = True
                part.save()

            messages.success(request, "Aircraft assembled successfully!")
            return redirect('aircrafts-list')

    else:
        form = AircraftAssembleForm(team=team)

    return render(request, 'aircrafts/aircraft_assemble.html', {'form': form})

class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    permission_class = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        profile = self.request.user.profile
        if profile.team.name != "Assembly Team":
            raise PermissionDenied("Only the Assembly Team can assemble aircraft.")
        
        aircraft_type = serializer.validated_data['aircraft_type']

        required_part_types = ['wing', 'fuselage', 'tail', 'avionics']
        
        parts_to_use = []
        
        for part_type in required_part_types:
            part = Part.objects.filter(
            part_type=part_type.capitalize(),
            aircraft_type=aircraft_type,
            quantity__gte=1
        ).first()
        if not part:
            raise ValidationError(f"Missing {part_type} for aircraft type {aircraft_type}")
        parts_to_use.append(part)

        
        with transaction.atomic():
            
            # Atomically decrease quantity using F()
            for part in parts_to_use:
                updated = Part.objects.filter(pk=part.pk, quantity__gte=1).update(quantity=F('quantity') - 1)
            if updated == 0:
                # This means no rows were updated due to insufficient stock
                raise ValidationError(f"Insufficient stock for {part.part_type}")

                
            serializer.save(assembled_by=self.request.user)
            
    def get_queryset(self):
        profile = self.request.user.profile
        if profile.team.name == "assembly Team":
            return Aircraft.objects.all()
        return Aircraft.objects.none()