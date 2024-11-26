function navigateToUrl(baseurl, dropdown) {
    const url = baseurl + dropdown.value;

    if (url) {
        window.location.href = url; // Redirects to the constructed URL
    }
}
