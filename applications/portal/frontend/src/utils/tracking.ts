
declare const window: any;

export function trackVendorClick(vendorName: string) {
  return () => {
    if (window.gtag) {
      window.gtag('event', 'vendor_click', {
        vendor_name: vendorName, // Track the vendor name
        value: vendorName,
      });
    }
  };
}