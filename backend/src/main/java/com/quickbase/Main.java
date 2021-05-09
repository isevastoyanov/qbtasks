package com.quickbase;

import com.quickbase.devint.*;
import org.apache.commons.lang3.tuple.Pair;

import java.util.*;

/**
 * The main method of the executable JAR generated from this repository. This is to let you
 * execute something from the command-line or IDE for the purposes of demonstration, but you can choose
 * to demonstrate in a different way (e.g. if you're using a framework)
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("Starting.");

        // The configurations below can be replaced by a Spring list of beans with @Ordered annotation where the
        // DB service is with highest order. That way it will be easier to add new data source.
        IStatService dbStatService = new DBManagerImpl();
        IStatService restStatService = new ConcreteStatService();

        List<IStatService> servicesByPriority = new ArrayList<>();
        servicesByPriority.add(dbStatService);
        servicesByPriority.add(restStatService);

        CountryNameCollisionResolver countryNameCollisionResolver = new HashMapCountryNameCollisionResolver();

        // DB data is with priority so the service data is added only if it's not already there
        Map<String, Integer> aggregatedData =
                aggregateDataWithPriority(servicesByPriority, countryNameCollisionResolver);
        // This is for debug purposes to see for any duplications
        System.out.println(new TreeMap<>(aggregatedData));
    }

    private static Map<String, Integer> aggregateDataWithPriority(
            List<IStatService> servicesByPriority,
            CountryNameCollisionResolver countryNameCollisionResolver) {
        if (servicesByPriority == null || servicesByPriority.size() == 0) {
            throw new IllegalArgumentException("This method should be called with at least one argument");
        }

        Map<String, Integer> aggregatedResult = new HashMap<>();
        for (IStatService statService : servicesByPriority) {
            for (Pair<String, Integer> pair : statService.getCountryPopulation()) {
                aggregatedResult.putIfAbsent(
                        countryNameCollisionResolver.getCountryName(pair.getKey()),
                        pair.getValue());
            }
        }

        return aggregatedResult;
    }
}