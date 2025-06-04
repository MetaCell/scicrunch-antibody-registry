
declare const window: any;

export function trackVendorClick(vendorName: string) {
    if (window.gtag) {
      window.gtag('event', 'click', {
        event_category: 'Vendor clicks',
        event_label: vendorName,
        vendor_name: vendorName, // Track the vendor name
        value: vendorName,
      });
    }
}