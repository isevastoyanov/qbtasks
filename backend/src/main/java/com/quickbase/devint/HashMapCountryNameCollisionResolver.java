package com.quickbase.devint;

import java.util.HashMap;
import java.util.Map;

/**
 * This class is used to resolve any known country name duplications. The map can be replaced by an external source
 * file like e.g. JSON or XML so it will be easier to add new known country name duplications.
 */
public class HashMapCountryNameCollisionResolver implements CountryNameCollisionResolver {
    private static final Map<String, String> COUNTRY_NAMES = new HashMap<>();

    static {
        COUNTRY_NAMES.put("United States of America", "USA");
        COUNTRY_NAMES.put("U.S.A.", "USA");
    }

    public String getCountryName(String countryName) {
        return COUNTRY_NAMES.getOrDefault(countryName, countryName);
    }
}
