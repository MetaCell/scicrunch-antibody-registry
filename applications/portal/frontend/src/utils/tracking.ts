
declare const window: any;

export function trackVendorClick(vendorName: string) {
  return () => {
    if (window.gtag) {
      window.gtag('event', 'click', {
        event_category: 'Vendor clicks',
        vendor_name: vendorName, // Track the vendor name
        value: vendorName,
      });
    }
  };
}