import numpy as np
import matplotlib.pyplot as plt

class EnergyStorageDevice:
    def __init__(self, name, energy_density, charge_rate, discharge_rate, self_discharge_rate):
        self.name = name
        self.energy_density = energy_density  # Wh/kg
        self.charge_rate = charge_rate  # C-rate
        self.discharge_rate = discharge_rate  # C-rate
        self.self_discharge_rate = self_discharge_rate  # % per day

    def charge(self, time):
        return min(1, self.charge_rate * time)

    def discharge(self, time):
        return min(1, self.discharge_rate * time)

    def self_discharge(self, time):
        return 1 - (self.self_discharge_rate / 100) * time

def compare_devices(devices, simulation_time):
    charge_profiles = []
    discharge_profiles = []
    self_discharge_profiles = []

    for device in devices:
        charge_profile = [device.charge(t) for t in range(simulation_time)]
        discharge_profile = [1 - device.discharge(t) for t in range(simulation_time)]
        self_discharge_profile = [device.self_discharge(t) for t in range(simulation_time)]
        
        charge_profiles.append(charge_profile)
        discharge_profiles.append(discharge_profile)
        self_discharge_profiles.append(self_discharge_profile)

    return charge_profiles, discharge_profiles, self_discharge_profiles

# Create energy storage devices
esc = EnergyStorageDevice("Electrolytic Super Capacitor", 800, 1, 1, 0.1)
supercapacitor = EnergyStorageDevice("Supercapacitor", 30, 100, 100, 20)
li_ion_battery = EnergyStorageDevice("Li-ion Battery", 250, 1, 1, 0.1)

devices = [esc, supercapacitor, li_ion_battery]

# Run simulation
simulation_time = 100
charge_profiles, discharge_profiles, self_discharge_profiles = compare_devices(devices, simulation_time)

# Plotting
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

for i, device in enumerate(devices):
    ax1.plot(charge_profiles[i], label=device.name)
    ax2.plot(discharge_profiles[i], label=device.name)
    ax3.plot(self_discharge_profiles[i], label=device.name)

ax1.set_title("Charge Profile")
ax1.set_xlabel("Time")
ax1.set_ylabel("State of Charge")
ax1.legend()

ax2.set_title("Discharge Profile")
ax2.set_xlabel("Time")
ax2.set_ylabel("State of Charge")
ax2.legend()

ax3.set_title("Self-Discharge Profile")
ax3.set_xlabel("Time (days)")
ax3.set_ylabel("Remaining Charge")
ax3.legend()

plt.tight_layout()
plt.show()

# Print energy density comparison
print("Energy Density Comparison:")
for device in devices:
    print(f"{device.name}: {device.energy_density} Wh/kg")