-- CreateTable
CREATE TABLE "User" (
    "user_id" UUID NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("user_id")
);

-- CreateTable
CREATE TABLE "Land" (
    "land_id" UUID NOT NULL,
    "latitude" DOUBLE PRECISION NOT NULL,
    "longitude" DOUBLE PRECISION NOT NULL,
    "land_size" DOUBLE PRECISION NOT NULL,
    "land_name" VARCHAR(100),
    "land_image" VARCHAR(200),
    "ph_level" DOUBLE PRECISION NOT NULL,
    "phosphorus" DOUBLE PRECISION NOT NULL,
    "potassium" DOUBLE PRECISION NOT NULL,
    "oxygen_level" DOUBLE PRECISION NOT NULL,
    "nitrogen" DOUBLE PRECISION NOT NULL,
    "user_id" UUID NOT NULL,

    CONSTRAINT "Land_pkey" PRIMARY KEY ("land_id")
);

-- CreateTable
CREATE TABLE "LandStatistic" (
    "land_stat_id" UUID NOT NULL,
    "land_use" DOUBLE PRECISION NOT NULL,
    "human_coverage" DOUBLE PRECISION NOT NULL,
    "water_availability" DOUBLE PRECISION NOT NULL,
    "distribution_optimality" DOUBLE PRECISION NOT NULL,
    "total_profit" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "land_id" UUID NOT NULL,

    CONSTRAINT "LandStatistic_pkey" PRIMARY KEY ("land_stat_id")
);

-- CreateTable
CREATE TABLE "Crop" (
    "crop_id" UUID NOT NULL,
    "crop_name" VARCHAR(30) NOT NULL,
    "crop_area" DOUBLE PRECISION NOT NULL,
    "crop_investment" DOUBLE PRECISION NOT NULL,
    "expected_money_return" DOUBLE PRECISION NOT NULL,
    "expected_weight_return" DOUBLE PRECISION NOT NULL,
    "land_id" UUID NOT NULL,

    CONSTRAINT "Crop_pkey" PRIMARY KEY ("crop_id")
);

-- CreateTable
CREATE TABLE "CropMaintenance" (
    "maintenance_id" UUID NOT NULL,
    "pesticide_level" DOUBLE PRECISION NOT NULL,
    "water_sufficienty" DOUBLE PRECISION NOT NULL,
    "land_id" UUID NOT NULL,

    CONSTRAINT "CropMaintenance_pkey" PRIMARY KEY ("maintenance_id")
);

-- CreateTable
CREATE TABLE "Finance" (
    "financial_id" UUID NOT NULL,
    "investment_amount" DOUBLE PRECISION,
    "expected_revenue" DOUBLE PRECISION,
    "land_id" UUID,

    CONSTRAINT "Finance_pkey" PRIMARY KEY ("financial_id")
);

-- CreateTable
CREATE TABLE "Weather" (
    "weather_id" UUID NOT NULL,
    "temperature" DOUBLE PRECISION NOT NULL,
    "humidity" DOUBLE PRECISION NOT NULL,
    "rainfall" DOUBLE PRECISION NOT NULL,
    "sunlight" DOUBLE PRECISION NOT NULL,
    "land_id" UUID,

    CONSTRAINT "Weather_pkey" PRIMARY KEY ("weather_id")
);

-- CreateTable
CREATE TABLE "BusinessPlan" (
    "business_plan_id" UUID NOT NULL,
    "executive_summary" TEXT NOT NULL,
    "resources" TEXT NOT NULL,
    "crops" TEXT NOT NULL,
    "weather_considerations" TEXT NOT NULL,
    "soil_maintenance" TEXT NOT NULL,
    "profit_estimations" TEXT NOT NULL,
    "other_recommendations" TEXT NOT NULL,
    "land_id" UUID NOT NULL,

    CONSTRAINT "BusinessPlan_pkey" PRIMARY KEY ("business_plan_id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Land_latitude_longitude_key" ON "Land"("latitude", "longitude");

-- CreateIndex
CREATE UNIQUE INDEX "LandStatistic_land_id_key" ON "LandStatistic"("land_id");

-- CreateIndex
CREATE UNIQUE INDEX "Crop_land_id_key" ON "Crop"("land_id");

-- CreateIndex
CREATE UNIQUE INDEX "CropMaintenance_land_id_key" ON "CropMaintenance"("land_id");

-- CreateIndex
CREATE UNIQUE INDEX "Finance_land_id_key" ON "Finance"("land_id");

-- CreateIndex
CREATE UNIQUE INDEX "Weather_land_id_key" ON "Weather"("land_id");

-- CreateIndex
CREATE UNIQUE INDEX "BusinessPlan_land_id_key" ON "BusinessPlan"("land_id");

-- AddForeignKey
ALTER TABLE "Land" ADD CONSTRAINT "Land_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("user_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "LandStatistic" ADD CONSTRAINT "LandStatistic_land_id_fkey" FOREIGN KEY ("land_id") REFERENCES "Land"("land_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Crop" ADD CONSTRAINT "Crop_land_id_fkey" FOREIGN KEY ("land_id") REFERENCES "Land"("land_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "CropMaintenance" ADD CONSTRAINT "CropMaintenance_land_id_fkey" FOREIGN KEY ("land_id") REFERENCES "Land"("land_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Finance" ADD CONSTRAINT "Finance_land_id_fkey" FOREIGN KEY ("land_id") REFERENCES "Land"("land_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Weather" ADD CONSTRAINT "Weather_land_id_fkey" FOREIGN KEY ("land_id") REFERENCES "Land"("land_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "BusinessPlan" ADD CONSTRAINT "BusinessPlan_land_id_fkey" FOREIGN KEY ("land_id") REFERENCES "Land"("land_id") ON DELETE RESTRICT ON UPDATE CASCADE;
