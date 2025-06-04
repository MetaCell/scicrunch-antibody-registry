
declare const window: any;

export function trackVendorClick(vendorName: string, vendorId: number) {
    if (window.gtag) {
      window.gtag('event', 'click', {
        event_category: 'Vendor clicks',
        event_label: `${vendorName} (${vendorId})`,
        vendor_name: vendorName, // Track the vendor name
        value: vendorName,
      });
    }
}