from h5py import File as h5File

sensors_explanation = {
    'PINP': 'Pump Intake Pressure',
    'PCAS': 'Casing Pressure',
    'PTUB': 'Tubing Pressure',
    'VDH': 'Pump Vibration',
    'TCPU': 'CPU Temperature',
    'EDH': 'Motor Voltage', # Actual voltage of the motor
    'PLIN': 'Line Pressure',
    'TVFD1': 'Heatsink Temperature',
    'EINPA': 'Input Voltage', # Input to the drive on surface
    'TINP': 'Intake Temperature',
    'IDH': 'Motor Current', # EHD Current
    'NSTART': 'Number of Starts',
    'JOUT': 'Output Power', # Output power of the drive
    'NPF': 'Power Factor',
    'YRUN': 'Run Status', # text
    'YSD': 'Last Shutdown Reason', # text
    'KRUNRSAC': 'Runtime Since Restart',
    'EVFD1OUT': 'Output Drive Voltage',
    'SVFD1OUT': 'Drive Frequency',
    'IMOUL': 'Motor Underload'
}


class H5_File:
    def __init__(self, filename):
        self.fp = h5File(filename, 'r', driver='core')

    def data_description(self):
        field_dict = {}
        for field in self.fp.keys():
            field_dict[field] = {}
            for esp in self.fp[field].keys():
                field_dict[field][esp] = list(self.fp[field][esp].keys())

        return field_dict

    def query(self, field, esp, sensor):
         return self.fp[field][esp][sensor]
