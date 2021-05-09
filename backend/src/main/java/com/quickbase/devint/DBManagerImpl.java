package com.quickbase.devint;

import org.apache.commons.lang3.tuple.ImmutablePair;
import org.apache.commons.lang3.tuple.Pair;

import java.sql.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * This DBManager implementation provides a connection to the database containing population data.
 * <p>
 * Created by ckeswani on 9/16/15.
 */
public class DBManagerImpl implements DBManager, IStatService {

    private static final String GET_COUNTRY_POPULATION_QUERY =
            "SELECT c.CountryName as country, SUM(cy.Population) as population " +
                    "FROM Country c " +
                    "JOIN State s ON c.CountryId = s.CountryId " +
                    "JOIN City cy ON s.StateId = cy.StateId " +
                    "GROUP BY c.CountryName;";

    @Override
    public Connection getConnection() {
        System.out.print("Getting DB Connection...");
        Connection connection = null;
        try {
            Class.forName("org.sqlite.JDBC");
            connection = DriverManager.getConnection("jdbc:sqlite:resources/data/citystatecountry.db");
            System.out.println("Opened database successfully");
        } catch (ClassNotFoundException cnf) {
            System.out.println("could not load driver");
        } catch (SQLException sqle) {
            System.out.println("sql exception:" + Arrays.toString(sqle.getStackTrace()));
        }

        return connection;
    }

    @Override
    public List<Pair<String, Integer>> getCountryPopulation() {
        List<Pair<String, Integer>> countryPopulation = new ArrayList<>();
        try (Connection connection = this.getConnection();
             Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(GET_COUNTRY_POPULATION_QUERY)) {
            while (rs.next()) {
                String country = rs.getString("country");
                int population = rs.getInt("population");
                countryPopulation.add(new ImmutablePair<>(country, population));
            }
        } catch (SQLException e) {
            System.out.println("sql exception:" + Arrays.toString(e.getStackTrace()));
        }

        return countryPopulation;
    }
}
