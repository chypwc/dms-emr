from pyspark.sql import SparkSession
import seaborn as sns
import matplotlib.pyplot as plt
from pyspark.sql.functions import when, col, max, count, sum as _sum
from pyspark.sql import functions as F

data_bucket = "source-bucket-chien"
database = "imba-raw"

spark = SparkSession.builder.appName("Features").getOrCreate()

order_products__train_df = spark.read \
    .format("awsdatacatalog") \
    .option("catalog", "AwsDataCatalog") \
    .option("database", database) \
    .option("table", "order_products__train") \
    .load()

order_products__prior_df = spark.read \
    .format("awsdatacatalog") \
    .option("catalog", "AwsDataCatalog") \
    .option("database", database) \
    .option("table", "order_products__prior") \
    .load()

orders_df = spark.read \
    .format("awsdatacatalog") \
    .option("catalog", "AwsDataCatalog") \
    .option("database", database) \
    .option("table", "orders") \
    .load()


products_df = spark.read \
    .format("awsdatacatalog") \
    .option("catalog", "AwsDataCatalog") \
    .option("database", database) \
    .option("table", "products") \
    .load()


departments_df = spark.read \
    .format("awsdatacatalog") \
    .option("catalog", "AwsDataCatalog") \
    .option("database", database) \
    .option("table", "departments") \
    .load()


aisles_df = spark.read \
    .format("awsdatacatalog") \
    .option("catalog", "AwsDataCatalog") \
    .option("database", database) \
    .option("table", "aisles") \
    .load()

order_products = order_products__prior_df.unionByName(order_products__train_df)


output_prefix = f"s3://{data_bucket}/parquet/"

# Save each DataFrame as Parquet
order_products.write.mode("overwrite").parquet(output_prefix + "order_products")
orders_df.write.mode("overwrite").parquet(output_prefix + "orders")
products_df.write.mode("overwrite").parquet(output_prefix + "products")
departments_df.write.mode("overwrite").parquet(output_prefix + "departments")
aisles_df.write.mode("overwrite").parquet(output_prefix + "aisles")